"""Passo 4.4a num comando so (caminho de sessao): o ORQUESTRADOR e este script, nao a janela da conversa.
Depois de `risk_triage.py export`, para cada lote sem veredito faz uma chamada headless em turno unico (sem
ferramenta) ao juiz barato (CLI `claude -p`), em paralelo; confere o formato, grava veredito_NNN.tsv e devolve UMA
linha por lote. Depois: risk_triage.py apply.

  python risk_triage_run.py <projeto> [--go] [--out PASTA] [--model haiku] [--jobs 6] [N ...]

Sem `--go` so LISTA os lotes que seriam julgados (cada chamada ao modelo e paga).

Sem N = todos os lotes ainda sem veredito. --out = gravar em outra pasta (teste; nao toca nos vereditos).
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import paths  # noqa: E402
import risk_triage  # noqa: E402

HEAD = ('NAO use ferramenta nenhuma. Em vez de escrever o arquivo veredito, responda com o conteudo exato que ele teria '
        '(uma linha `id<TAB>motivo` por fala apontada), sem cercas de codigo e sem texto antes ou depois. '
        'Nada a apontar: responda so com a palavra VAZIO.\n\n')


def parse(reply, ids):
    """-> (linhas validas, linhas descartadas). Valida = id do lote + motivo."""
    good, bad = [], 0
    for ln in reply.splitlines():
        f = ln.strip().split('\t')
        if len(f) >= 2 and f[0] in ids:
            good.append(f[0] + '\t' + f[1])
        elif ln.strip() and ln.strip() != 'VAZIO':
            bad += 1
    return good, bad


def one(n, out, model, d):
    r = ''
    for _ in range(3):            # resposta fora do formato: tenta de novo, ate 3 vezes
        r = _one(n, out, model, d)
        if 'FALHOU' not in r:
            break
    return r


def _one(n, out, model, DIR):
    lot = (DIR / f'lote_{n:03d}.tsv').read_text(encoding='utf-8')
    ids = {ln.split('\t')[0] for ln in lot.splitlines() if ln.strip()}
    prompt = HEAD + (DIR / 'triagem_prompt.md').read_text(encoding='utf-8') + f'\n\n## lote_{n:03d}.tsv\n\n' + lot
    exe = shutil.which('claude')
    if not exe:
        return f'lote {n:03d} FALHOU: comando `claude` nao esta no PATH (instale o Claude Code ou ajuste o PATH)'
    try:
        p = subprocess.run([exe, '-p', '--model', model, '--output-format', 'json', '--allowedTools', ''],
                           input=prompt, capture_output=True, text=True, encoding='utf-8', errors='replace',
                           timeout=900)
    except subprocess.TimeoutExpired:
        return f'lote {n:03d} FALHOU: `claude` sem resposta em 900 s'
    try:
        j = json.loads(p.stdout)
    except ValueError:
        return f'lote {n:03d} FALHOU: resposta nao e JSON (exit {p.returncode})'
    (out / f'resposta_{n:03d}.txt').write_text(j.get('result', ''), encoding='utf-8')   # bruto, para diagnostico
    good, bad = parse(j.get('result', ''), ids)
    if bad:                       # resposta fora do formato nao vira veredito: rodar de novo
        return f'lote {n:03d} FALHOU: {bad} linha(s) fora do formato; nada gravado'
    (out / f'veredito_{n:03d}.tsv').write_text(''.join(g + '\n' for g in good), encoding='utf-8')
    return f'lote {n:03d} ok | falas {len(ids)} | apontadas {len(good)} | ${j.get("total_cost_usd", 0):.3f}'


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('project')
    ap.add_argument('lots', nargs='*', type=int)
    ap.add_argument('--out')
    ap.add_argument('--model', default='haiku')
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--go', action='store_true', help='chama o modelo (pago); sem isso so lista os lotes')
    a = ap.parse_args()
    src = risk_triage._dir(paths.require_project(a.project))
    out = pathlib.Path(a.out) if a.out else src
    lots = a.lots or [int(f.stem[5:]) for f in sorted(src.glob('lote_*.tsv'))
                      if not (out / f.name.replace('lote_', 'veredito_')).is_file()]
    if not a.go:
        print(f'{len(lots)} lote(s) sem veredito: {lots}  (use --go para chamar o modelo, pago)')
        return
    out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        for line in ex.map(lambda n: one(n, out, a.model, src), lots):
            print(line, flush=True)


if __name__ == '__main__':
    main()
