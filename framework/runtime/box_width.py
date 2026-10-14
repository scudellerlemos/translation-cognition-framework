"""Largura de linha por caixa, derivada do INGLES do proprio jogo (nao um 62 fixo).

O ingles ja roda no jogo: o maior segmento visivel entre quebras que ele exibe e a largura provada da caixa.
No bof4 um limite fixo de 62 nunca disparava onde importa (e marcava milhares de falas que cabem).

  project.json  "line_width": "derive"        -> usa o maior segmento visivel do texto-fonte do projeto
                "line_width_max": N           -> N fixo (vence o derive)
                (nenhum dos dois)             -> 62, o padrao antigo
  python box_width.py <projeto>               mostra o limite e a distribuicao do ingles
  rewrap(texto, limite)                       requebra mecanicamente nos espacos (passo do pipeline)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifact_io  # noqa: E402
import context_pack  # noqa: E402
import model  # noqa: E402
import opcodes  # noqa: E402
import paths  # noqa: E402

DEFAULT = 62
_SPLIT = re.compile("|".join(map(re.escape, (context_pack.TOKEN, chr(10), " // "))))
_VISIBLE = re.compile(r"\{c-?\d*\}|\{W\d+\}|\{COLOR\}|\{END\}")


def widths(text: str, tbl: dict) -> list[int]:
    """Largura visivel de cada segmento (entre quebras de caixa). Com tabela de opcodes do conector usa-a
    (parametro nao e codigo; variavel tem largura); sem tabela, cai no token `\n` do framework."""
    if tbl:
        return [w for w, t in opcodes.segments(text, tbl) if t.strip() or w]
    return [model._translit_len(_VISIBLE.sub("", x)) for x in _SPLIT.split(text or "") if x.strip()]


def derive(root) -> int:
    """Maior segmento visivel das falas que o autor quebrou em 2+ linhas (0 se nao ha nenhuma): a largura
    mostra a caixa; texto corrido e quebrado pelo motor e nao diz nada."""
    best, tbl = 0, opcodes.table(root)
    for scene in artifact_io.scenes(root):
        for ln in artifact_io.plan_lines(root, scene):
            w = widths(ln.get("text_source", ""), tbl)
            if len(w) > 1:
                best = max(best, *w)
    return best


def limit(root) -> int:
    cfgp = paths.project_json(root)
    cfg = json.loads(cfgp.read_text(encoding="utf-8")) if cfgp.is_file() else {}
    if cfg.get("line_width_max"):
        return int(cfg["line_width_max"])
    if cfg.get("line_width") == "derive":
        return derive(root) or DEFAULT
    return DEFAULT


def configure(root) -> int:
    """Aplica o limite do projeto onde a largura ja e usada (quality_review.WIDTH_MAX) e o devolve."""
    import quality_review
    quality_review.WIDTH_MAX = n = limit(root)
    return n


def rewrap(text: str, width: int, token: str = r"\n") -> str:
    """Requebra `text` (um bloco sem quebras proprias) nos espacos para nenhum segmento passar de `width`.
    Palavra maior que `width` fica inteira (nao se corta palavra)."""
    out, cur = [], ""
    for w in text.split(" "):
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    out.append(cur)
    return token.join(out)


def main():
    if {"-h", "--help"} & set(sys.argv[1:]):
        print(__doc__)
        return
    root = paths.require_project(sys.argv[1] if len(sys.argv) > 1 else "")
    print(f"limite do projeto: {limit(root)} | derivado do ingles: {derive(root)} | padrao: {DEFAULT}")


if __name__ == "__main__":
    main()
