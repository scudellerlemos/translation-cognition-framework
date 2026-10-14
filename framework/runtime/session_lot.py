"""Caminho da SESSAO em lote (a IA da sessao traduz; nada vai a API): prompt de varias cenas num so arquivo,
conferencia mecanica e fechamento pelo run_scene. Passos de apoio: `plan` (agrupa cenas em lotes), `split`/`join`
(divide um lote grande por secao), `install` (copia os .DAT remontados para o jogo). Os arquivos de trabalho ficam
em `projects/<p>/tools_local/` (gitignored: trazem fala do jogo).

  session_lot.py <projeto> plan <saida.json> [--max N]      lotes de ate N falas (150), textos repetidos so 1x
  session_lot.py <projeto> prompt <id> [--dedup] [--short-carta] [--tm-cap N] [--no-lore] [--tsv|--tsv4] CENA...
      junta os scene_prompt.md num prompt de lote: tools_local/lot_<id>.md (+ lot_<id>.meta.json)
  session_lot.py <projeto> check <id> CENA...   confere tokens, orcamento de bytes e cobertura das traducoes
  session_lot.py <projeto> go <id> CENA...      converte lot_<id>.tsv (se existir), replica falas deduplicadas,
                              confere e, se limpo, roda o run_scene (`--backend in-session --require-back`)
  session_lot.py <projeto> split|join <id>      divide/junta um lote por secao do offset
  session_lot.py <projeto> install <output> <source_dat> <pasta DAT do jogo> [--go]
"""
import filecmp
import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import budget  # noqa: E402
import context_pack  # noqa: E402
import opcodes  # noqa: E402
import paths  # noqa: E402

ROOT = TMP = None            # definidos por _init(projeto)
CFG = {}                     # project.json (excecoes de orcamento)
BR = '[01]'                  # token de quebra de linha (o `newline` da tabela de opcodes)
TOK = re.compile(r'\[[0-9A-Fa-f]{2}\]')
ROW = re.compile(r'^\| (\S+:\d+:\d+) \| (\d*) \| (.*) \|$')
CARTA = """## 1. CARTA DE GOVERNANCA (resumo para o tradutor)
- Voz: se o personagem tem marcador de voz na secao 4 (arcaico, tu, 3a pessoa, giria), TODA fala segue o marcador.
- Sem marcador: pt-BR contemporaneo natural, o que um jogador de hoje diria; sem arcaismo gratuito.
- Lore: termos do glossario na forma certa. Spoiler: nada revelado antes da hora; preserve ambiguidade do original.
- Situacao: traduza pela emocao/intencao da cena; interjeicao e onomatopeia sao traducao (localizar, nao copiar).
- Naturalidade: um nativo le NESTA situacao e entende facil; a juncao de linhas quebradas soa natural.
- Conector: cabe no orcamento de bytes e preserva todos os tokens.
- Metadados REAIS por fala (speaker, tone_register, intent, risk_level), nao texto padrao.
- Risco calibrado: identidade dupla, comedia, 1a mencao de lore, spoiler -> high. Risco >= medium exige risk_notes.
"""
TSV = """## 8. Formato de saida EXIGIDO
Escreva UM arquivo so, `{path}`, texto puro UTF-8: uma fala por linha, 7 campos separados por TAB, sem cabecalho:
`offset<TAB>speaker<TAB>tone_register<TAB>intent<TAB>risk_level<TAB>risk_notes<TAB>traducao`
- speaker: nome EN exato da secao 4 para personagem conhecido; `npc`, `system` ou `unknown` nos demais.
- risk_level: low|medium|high|critical; risk_notes vazio se low. A traducao leva os tokens `[xx]` exatos.
- Cobrir TODOS os offsets das tabelas da secao 7. O comando converte o arquivo nos JSON de cada cena.
"""
TSV4 = """## 8. Formato de saida EXIGIDO
Escreva UM arquivo so, `{path}`, texto puro UTF-8: uma fala por linha, 4 campos separados por TAB, sem cabecalho:
`offset<TAB>speaker<TAB>risk_level<TAB>traducao`
- speaker: nome EN exato da secao 4 para personagem conhecido; `npc`, `system` ou `unknown` nos demais.
- risk_level: low|medium|high|critical (identidade dupla, comedia, 1a mencao de lore, spoiler -> high).
- A traducao leva os tokens `[xx]` exatos. Cobrir TODOS os offsets das tabelas da secao 7.
"""


def scene_of(off):
    return off.split('.DAT')[0]


def cmd_prompt(lot, scenes, flags):
    docs = {s: re.split(r'(?m)^(?=## )', (paths.scene_dir(ROOT, s) / 'scene_prompt.md').read_text(encoding='utf-8'))
            for s in scenes}
    head = lambda sec: sec.split('\n', 1)[0]
    order = []
    for parts in docs.values():
        for sec in parts[1:]:
            if head(sec) not in order:
                order.append(head(sec))
    cap = int(flags.get('--tm-cap', 0))
    L = [f'# Lote de {len(scenes)} cenas: {" ".join(scenes)}', '',
         'As secoes abaixo valem para TODAS as cenas do lote. As linhas a traduzir vem por cena, na secao 7.', '']
    dup, seen_src, offsets, in_carta = {}, {}, [], False
    for h in order:
        bodies = [sec for parts in docs.values() for sec in parts[1:] if head(sec) == h]
        if '--short-carta' in flags:            # da "## 1. CARTA" ate antes da "## 2."
            if h.startswith('## 1.'):
                in_carta = True
                L.append(CARTA)
            elif re.match(r'## \d', h):
                in_carta = False
            if in_carta:
                continue
        if '--no-lore' in flags and (h.startswith('## 5.') or h.startswith('## 5d')):
            continue
        if ('--tsv' in flags or '--tsv4' in flags) and h.startswith('## 8.'):
            L.append((TSV4 if '--tsv4' in flags else TSV).format(path=str(TMP / f'lot_{lot}.tsv')))
            continue
        if h.startswith('## 7.'):
            first = True
            for s, parts in docs.items():
                sec = next(x for x in parts[1:] if head(x) == h)
                body = sec.split('\n', 1)[1].split('\n')
                rows = [i for i, x in enumerate(body) if ROW.match(x)]
                done = _load(s)['lines'] if '--skip-done' in flags else {}   # ja preenchida pelo reuso da memoria
                keep = body[:rows[0] - 2] if first else []      # aviso de orcamento so na 1a cena
                keep += ['| offset | byte_budget | source |', '|---|---|---|']
                for i in rows:
                    off, bud, src = ROW.match(body[i]).groups()
                    if off in done:
                        continue
                    if '--dedup' in flags and src in seen_src:
                        canon = seen_src[src]
                        dup[off] = canon['off']
                        if bud and (not canon['bud'] or int(bud) < int(canon['bud'])):
                            canon['bud'] = bud                  # a traducao unica tem de caber no menor orcamento
                        continue
                    seen_src[src] = row = {'off': off, 'bud': bud, 'src': src}
                    offsets.append(off)
                    keep.append(row)
                L += [f'## 7. Linhas a traduzir -- cena {s}'] + keep + ['']
                first = False
        elif len(set(bodies)) == 1 and len(bodies) == len(docs):
            L.append(bodies[0])
        else:
            seen, keep, n = set(), [h], 0
            for b in bodies:
                for line in b.split('\n')[1:]:
                    if line.strip() and line in seen:
                        continue
                    if line.startswith('**'):
                        n = 0
                    if cap and h.startswith('## 6.') and line.startswith('- ') and not _in_exact(keep):
                        n += 1
                        if n > cap:
                            continue
                    seen.add(line)
                    keep.append(line)
            L.append(re.sub(r'\n{3,}', '\n\n', '\n'.join(keep)) + '\n')
    text = '\n'.join(f'| {x["off"]} | {x["bud"]} | {x["src"]} |' if isinstance(x, dict) else x for x in L)
    if dup:
        text = text.replace('As linhas a traduzir vem por cena, na secao 7.',
                            'As linhas a traduzir vem por cena, na secao 7. Fala repetida no lote aparece UMA vez '
                            '(o comando replica nas demais cenas): traduza so o que esta nas tabelas.')
    (TMP / f'lot_{lot}.md').write_text(text, encoding='utf-8')
    (TMP / f'lot_{lot}.meta.json').write_text(json.dumps({'dup': dup, 'offsets': offsets}), encoding='utf-8')
    tot = sum(len(''.join(p)) for p in docs.values())
    print(f'lot_{lot}.md: {len(text)} chars (separados: {tot}) | falas na tabela {len(offsets)} | deduplicadas {len(dup)}')


def _in_exact(keep):
    """True se o ultimo cabecalho em negrito da secao 6 e o das falas IDENTICAS (essas nunca sao cortadas)."""
    last = next((x for x in reversed(keep) if x.startswith('**')), '')
    return 'identicas' in last


def _load(s):
    p = paths.translations(ROOT, s, context_pack.scene_id_of(s))
    return json.loads(p.read_text(encoding='utf-8')) if p.is_file() else {'lines': {}}


def _save(s, data):
    paths.translations(ROOT, s, context_pack.scene_id_of(s)).write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')


# palavra que nao pode ficar pendurada no fim da linha (artigo, preposicao, conjuncao, pronome atono)
_FUNC = set('o a os as um uma uns umas de do da dos das em no na nos nas por pelo pela para pra com sem e ou que se '
            'me te lhe vos ao aos à às meu minha seu sua teu tua este esta esse essa aquele aquela mas nem'.split())


def rebreak(src, t, br='[01]'):
    """Quebra de linha perdida/sobrando: troca espaco<->[01] ate a contagem bater com o original (1 byte por 1 byte,
    o orcamento nao muda). Repoe no maior trecho, mirando fracoes iguais; entre os espacos perto do alvo prefere o
    que vem depois de pontuacao e evita artigo/preposicao pendurado no fim da linha. Medido em 377 falas reprovadas:
    resolve 94% sem chamar o modelo; palavra pendurada 2% (o proprio modelo deixa em 43%).
    ponytail: nao conhece a largura da caixa; 1 em 354 passou da maior linha do original -- se estourar no jogo,
    passar a largura do conector e descartar o espaco que a ultrapassa."""
    need = src.count(br) - t.count(br)

    def cost(seg, i, target):
        prev = seg[:i].rsplit(' ', 1)[-1]
        if prev[-1:] in ',.;:!?…':
            return abs(i - target) - 5
        return abs(i - target) + (6 if TOK.sub('', prev).strip('"\'(').lower() in _FUNC else 0)
    while need > 0:
        segs, pos = [], 0
        for seg in t.split(br):
            segs.append((pos, seg)); pos += len(seg) + len(br)
        start, seg = max(segs, key=lambda x: len(TOK.sub('', x[1])))
        sp = [i for i, c in enumerate(seg) if c == ' ']
        if not sp:
            return t
        target = len(seg) / (need + 1) if len(segs) == 1 else len(seg) / 2
        i = min(sp, key=lambda i: cost(seg, i, target))
        cut = start + i + len(br)
        t = t[:start + i] + br + t[start + i + 1:]
        need -= 1
        if len(segs) == 1 and need > 0:                 # o resto vai no trecho da direita, de novo em fracoes iguais
            return t[:cut] + rebreak(br * need, t[cut:], br)
    while need < 0 and br in t:
        i = t.rfind(br)
        t = t[:i] + ' ' + t[i + len(br):]
        need += 1
    return t


def cmd_check(lot, scenes, run):
    meta = json.loads((TMP / f'lot_{lot}.meta.json').read_text(encoding='utf-8'))
    data = {s: _load(s) for s in scenes}
    tsv = TMP / f'lot_{lot}.tsv'
    bad = []
    if run and tsv.is_file():
        for n, line in enumerate(tsv.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            f = line.split('\t')
            if len(f) == 4:                         # formato curto: offset, speaker, risk_level, traducao
                f = [f[0], f[1], '', '', f[2], '', f[3]]
            if len(f) != 7 or scene_of(f[0]) not in data:
                bad.append(f'tsv linha {n}: {len(f)} campos (esperado 4 ou 7) ou offset de cena fora do lote')
                continue
            data[scene_of(f[0])]['lines'][f[0]] = dict(zip(
                ('speaker', 'tone_register', 'intent', 'risk_level', 'risk_notes', 't'), f[1:], strict=False))
    if run:
        for d, c in meta['dup'].items():
            e = data[scene_of(c)]['lines'].get(c)
            if e and d not in data[scene_of(d)]['lines']:
                data[scene_of(d)]['lines'][d] = dict(e)
        for s in scenes:
            _save(s, data[s])
    want = set(meta['offsets']) | set(meta['dup'])
    moved = 0
    for s in scenes:
        pack = json.loads(paths.pack(ROOT, s).read_text(encoding='utf-8'))
        lines = data[s]['lines']
        for r in pack['lines']:
            off, e = r['offset'], lines.get(r['offset'])
            if e is None:
                if off in want:
                    bad.append(f'{off}: sem traducao')
                continue
            t, src = e.get('t', ''), r['source']
            # original que termina em [00] + espaco: sem o espaco o [00] vira o fim da string e o round-trip falha
            end = re.search(r'\[00\]\s*$', src)
            if end and not t.endswith(end.group()):
                if run and t.rstrip().endswith('[00]'):
                    e['t'] = t = t.rstrip() + end.group()[4:]
                else:
                    bad.append(f'{off}: precisa terminar como o original ({end.group()!r})')
            if run and sorted(TOK.findall(t)) != sorted(TOK.findall(src)):
                t2 = rebreak(src, t, BR)
                if sorted(TOK.findall(t2)) == sorted(TOK.findall(src)):
                    e['t'] = t = t2
                    moved += 1
            if sorted(TOK.findall(t)) != sorted(TOK.findall(src)):
                bad.append(f'{off}: tokens {sorted(TOK.findall(t))} != original {sorted(TOK.findall(src))}')
            pc = pack.get('project_constraints', {})
            bb = r.get('byte_budget') and budget.effective_budget(off, int(r['byte_budget']), CFG)
            if bb and budget.over_budget(t, bb, pc, token_rx=TOK):
                bad.append(f"{off}: {budget.budget_len(t, pc, TOK)} bytes > {budget.usable(bb, pc)} "
                           "(conta de budget.py; token conta 1 byte)")
            if e.get('risk_level', 'low') not in ('low', 'medium', 'high', 'critical'):
                bad.append(f'{off}: risk_level invalido')
        bad += [f'{o}: offset nao existe na cena' for o in lines if o not in {r['offset'] for r in pack['lines']}]
    if moved:
        for s in scenes:
            _save(s, data[s])
        print(f'CONFERENCIA: {moved} quebra(s) [01] reposta(s) mecanicamente')
    if bad:
        print(f'CONFERENCIA: {len(bad)} problema(s) -- corrija e rode de novo:')
        print('\n'.join(bad[:60]))
        sys.exit(1)
    print(f'CONFERENCIA: ok ({sum(len(d["lines"]) for d in data.values())} falas)')
    if run:
        p = subprocess.run([sys.executable, str(HERE / 'run_scene.py'), str(ROOT), *scenes,
                            '--backend', 'in-session', '--require-back'],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        keep = re.compile(r'AGUARDANDO|SCHEMA|ERRO|offsets|token|overflow|LOTE|status final')
        print('\n'.join(x[:240] for x in (p.stdout + p.stderr).splitlines() if keep.search(x)))


def _init(project):
    global ROOT, TMP, TOK, BR, CFG
    ROOT = paths.require_project(project)
    TMP = ROOT / 'tools_local'
    TMP.mkdir(exist_ok=True)
    CFG = json.loads(paths.project_json(ROOT).read_text(encoding='utf-8'))
    pats = CFG.get('formatting_token_patterns')
    TOK = re.compile(pats[0]) if pats else TOK
    BR = next((f'[{c}]' for c, v in opcodes.table(ROOT).items() if v['name'] == 'newline'), BR)
    return ROOT


def cmd_plan(out, max_lines=150):
    """Lotes por ordem de cena nao verificada; cena grande (>100 falas) vai sozinha; texto igual (scene_dedup) so 1x."""
    import csv

    import scene_dedup
    st = json.loads(paths.run_state(ROOT).read_text(encoding='utf-8')).get('scenes', {}) if paths.run_state(ROOT).is_file() else {}
    dups = scene_dedup.groups(ROOT)
    skip = {d for ds in dups.values() for d in ds}
    lots, cur, n = [], [], 0
    for sc in sorted(d.name for d in paths.scenes_dir(ROOT).iterdir() if paths.dialogs(ROOT, d.name).is_file()):
        if sc in skip or st.get(sc, {}).get('status') == 'verified':
            continue
        with paths.dialogs(ROOT, sc).open(encoding='utf-8-sig', newline='') as fh:
            size = sum(1 for _ in csv.DictReader(fh))
        if size > 100:
            lots.append({'scenes': [sc], 'lines': size})
            continue
        if n + size > max_lines and cur:
            lots.append({'scenes': cur, 'lines': n})
            cur, n = [], 0
        cur.append(sc)
        n += size
    if cur:
        lots.append({'scenes': cur, 'lines': n})
    pathlib.Path(out).write_text(json.dumps({'lots': lots, 'dups': dups}, indent=1), encoding='utf-8')
    print(len(lots), 'lotes;', sum(len(v) for v in dups.values()), 'copias em', len(dups), 'grupos (scene_dedup.py copy leva a traducao)')


def cmd_install(out, src, game, go):
    """Instala no jogo os .DAT de `out` que diferem do original. .bak so se nao existir e so de arquivo identico ao
    original; confere a copia no fim."""
    out, src, game = map(pathlib.Path, (out, src, game))
    new = same = 0
    for f in sorted(out.glob('*.DAT')):
        if not (src / f.name).is_file() or filecmp.cmp(f, src / f.name, shallow=False):
            continue                                    # cena nao traduzida: output == original
        g, bak = game / f.name, game / (f.name + '.bak')
        if filecmp.cmp(f, g, shallow=False):
            same += 1
            continue
        if not bak.exists():
            assert filecmp.cmp(g, src / f.name, shallow=False), f'{f.name}: jogo != original e sem .bak'
            if go:
                shutil.copy2(g, bak)
        else:
            assert filecmp.cmp(bak, src / f.name, shallow=False), f'{f.name}: .bak != original'
        if go:
            shutil.copy2(f, g)
            assert filecmp.cmp(f, g, shallow=False), f.name
        new += 1
        print(('instalado ' if go else 'a instalar ') + f.name + ('' if bak.exists() else ' (+.bak)'))
    print(f'{new} arquivo(s) {"instalados" if go else "a instalar"}, {same} ja em dia')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    _init(sys.argv[1])
    cmd, rest = sys.argv[2], sys.argv[3:]
    if cmd == 'plan':
        cmd_plan(rest[0], int(rest[rest.index('--max') + 1]) if '--max' in rest else 150)
    elif cmd == 'install':
        cmd_install(*rest[:3], go='--go' in rest)
    elif cmd in ('split', 'join'):
        import session_part
        getattr(session_part, cmd)(TMP, rest[0])
    else:
        lot, rest = rest[0], rest[1:]
        flags, scenes, it = {}, [], iter(rest)
        for a in it:
            if a == '--tm-cap':
                flags[a] = next(it)
            elif a.startswith('--'):
                flags[a] = True
            else:
                scenes.append(a)
        if cmd == 'prompt':
            cmd_prompt(lot, scenes, flags)
        else:
            cmd_check(lot, scenes, run=(cmd == 'go'))
