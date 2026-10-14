"""Tabela de opcodes do conector, com parametros, usada por todo passo que MEDE ou EDITA texto com codigos.

Em `project.json` -> `connector.control_codes`, cada codigo e o nome (forma curta) ou um objeto:
    "01": "newline"
    "07": {"name": "var_value", "params": 1, "width": 3, "values": ["00", "03", "07"]}
  name    papel: `newline`, `page_break` e `choice_start` (abre o menu) quebram a caixa; qualquer outro nome nao quebra
  params  quantos tokens `[xx]` seguintes sao parametro do codigo (nao sao codigos); padrao 0
  width   glifos que o codigo exibe na tela (variavel como numero/nome); padrao 0
  values  valores possiveis do parametro (documenta e valida); vazio = livre
O corte ingenuo (cada `[xx]` e um codigo) corrompe `[07][03]`: o `[03]` e valor do 07, nao quebra.

  segments(text, table) -> [(largura_visivel_em_glifos, texto_do_segmento)] entre quebras de caixa
"""
import json
import re
from pathlib import Path

_TOK = re.compile(r"\[([0-9A-Fa-f]{2})\]")
BREAKS = ("newline", "page_break", "choice_start")   # choice_start: o menu e outra janela, nao continua a linha do dialogo


def table(root) -> dict:
    """{CODIGO_MAIUSCULO: {name, params, width, values}} do project.json (vazio se nao ha tabela)."""
    p = Path(root) / "project.json"
    raw = (json.loads(p.read_text(encoding="utf-8")).get("connector", {}).get("control_codes", {})
           if p.is_file() else {})
    out = {}
    for k, v in raw.items():
        v = {"name": v} if isinstance(v, str) else dict(v)
        out[k.upper()] = {"name": v.get("name", ""), "params": int(v.get("params", 0)),
                          "width": int(v.get("width", 0)), "values": [x.upper() for x in v.get("values", [])]}
    return out


def tokens(text: str, tbl: dict) -> list[tuple]:
    """Quebra `text` em ('text', s) e ('code', CODIGO, [parametros]); os parametros saem do fluxo de codigos."""
    out, pos = [], 0
    ms = list(_TOK.finditer(text or ""))
    i = 0
    while i < len(ms):
        m = ms[i]
        if m.start() > pos:
            out.append(("text", text[pos:m.start()]))
        code = m.group(1).upper()
        n = tbl.get(code, {}).get("params", 0)
        params, end = [], m.end()
        j = i + 1
        while len(params) < n and j < len(ms) and ms[j].start() == end:   # parametro vem colado ao codigo
            params.append(ms[j].group(1).upper())
            end = ms[j].end()
            j += 1
        out.append(("code", code, params))
        pos, i = end, j
    if pos < len(text or ""):
        out.append(("text", text[pos:]))
    return out


def invalid_params(text: str, tbl: dict) -> list[str]:
    """Codigos cujo parametro nao esta em `values` (quando a tabela lista os valores possiveis)."""
    bad = []
    for t in tokens(text, tbl):
        if t[0] == "code":
            vals = tbl.get(t[1], {}).get("values", [])
            if vals and any(p not in vals for p in t[2]):
                bad.append(f"[{t[1]}]{''.join(f'[{p}]' for p in t[2])}")
    return bad


def segments(text: str, tbl: dict) -> list[tuple[int, str]]:
    """Segmentos entre quebras de caixa, com a largura em glifos (texto + `width` dos codigos de variavel)."""
    segs, cur, w = [], "", 0
    for t in tokens(text, tbl):
        if t[0] == "text":
            cur += t[1]
            w += len(t[1])
        elif tbl.get(t[1], {}).get("name") in BREAKS:
            segs.append((w, cur))
            cur, w = "", 0
        else:
            w += tbl.get(t[1], {}).get("width", 0)
    segs.append((w, cur))
    return segs
