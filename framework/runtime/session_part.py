"""Divide um prompt de lote grande por secao do arquivo (caminho da sessao); chamado por session_lot.py.

  split <id>   lot_<id>.md -> lot_<id>_<secao>.md (um por secao do offset), cada um com so as suas falas,
                       a lista dos nomes de keep_names.txt (nomes que ficam no original) que aparecem nelas e a saida lot_<id>_<secao>.tsv
  join <id>    junta os lot_<id>_<secao>.tsv em lot_<id>.tsv (para o `lot.py go`)
"""
import pathlib
import re

ROW = re.compile(r'^\| \S+:(\d+):\d+ \| ')
NOTE = """## 7a. Texto de SISTEMA (menu, ajuda de batalha, bestiario) -- regras deste lote
- NAO e dialogo: speaker `system`, risco `low` salvo duvida real. Frase curta, direta, de manual de jogo.
- O orcamento de bytes (coluna byte_budget) e o alvo de cada fala (a conta esta em budget.py);
  o conferir do lote aponta o que passa. Se nao couber, abrevie com ponto ("Def.", "Pes.").
- Rotulo curto de menu (uma ou duas palavras, sem pontuacao) vai SEM acento; frase e descricao vao com acento normal.
- Nome de item, arma, armadura, acessorio, habilidade e inimigo FICA EM INGLES, identico ao original.
  Nomes que aparecem neste lote: {names}
- Palavra destacada entre [05][xx] e [06] que nao esta na lista acima e termo comum: traduza.
- Mesma palavra do original = mesma traducao no lote inteiro (atributos, estados, elementos, comandos).
"""


def split(TMP: pathlib.Path, lot: str) -> None:
    src = (TMP / f'lot_{lot}.md').read_text(encoding='utf-8').splitlines()
    a = next((i for i, x in enumerate(src) if x.startswith('## 7.')), None)
    b = next((i for i, x in enumerate(src) if x.startswith('## 8.')), None)
    if a is None or b is None or b < a:
        raise ValueError(f"lot_{lot}.md sem as secoes '## 7.' e '## 8.' (nessa ordem): nada a dividir")
    rows = [x for x in src[a:b] if ROW.match(x)]
    head = [x for x in src[a:b] if not ROW.match(x)]
    kn = TMP / 'keep_names.txt'
    names = [n for n in kn.read_text(encoding='utf-8').splitlines() if n.strip()] if kn.is_file() else []
    for sec in sorted({ROW.match(x).group(1) for x in rows}, key=int):
        mine = [x for x in rows if ROW.match(x).group(1) == sec]
        text = '\n'.join(mine)
        used = [n for n in names if re.search(r'(?<!\w)' + re.escape(n) + r'(?!\w)', text)]
        tail = '\n'.join(src[b:]).replace(f'lot_{lot}.tsv', f'lot_{lot}_{sec}.tsv')
        out = src[:a] + NOTE.format(names='; '.join(used) or '(nenhum)').splitlines() + [''] + head + mine + ['', tail]
        (TMP / f'lot_{lot}_{sec}.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
        print(f'lot_{lot}_{sec}.md: {len(mine)} falas, {len(used)} nomes, {sum(map(len, out))} chars')


def join(TMP: pathlib.Path, lot: str) -> None:
    parts = sorted(TMP.glob(f'lot_{lot}_*.tsv'))
    lines = [x for p in parts for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
    (TMP / f'lot_{lot}.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'lot_{lot}.tsv: {len(lines)} falas de {len(parts)} parte(s)')
