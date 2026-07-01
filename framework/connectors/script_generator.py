"""
script_generator.py — gerador de candidato de conector para engines T2.

D1 stub: renderiza o skeleton com os valores detectados pelo evidence_collector
preenchidos como comentários orientadores. O dev (ou o LLM em D2) completa o
restante.

Para T1, este módulo não é chamado — o conector de referência é reutilizado diretamente.
Para T2, gera um ponto de partida que documenta o que foi detectado.
"""
from __future__ import annotations

from pathlib import Path

_SKELETON = Path(__file__).resolve().parent / "_skeleton" / "extract.py"


def generate(evidence: dict, engine_hint: str | None = None) -> str:
    """Gera candidato de extract.py para engines T2.

    Preenche o skeleton com as evidências detectadas como comentários orientadores.
    O resultado NÃO é um conector funcional — é um ponto de partida documentado.

    Retorna a string do conteúdo do arquivo gerado.
    """
    skeleton = _SKELETON.read_text(encoding="utf-8") if _SKELETON.is_file() else _FALLBACK_SKELETON

    header = _render_header(evidence, engine_hint)
    return header + skeleton


def _render_header(evidence: dict, engine_hint: str | None) -> str:
    lines = [
        "# GERADO AUTOMATICAMENTE por script_generator.py (D1 stub — completar manualmente)",
        "#",
        "# Evidências detectadas pelo evidence_collector:",
        f"#   file_count      : {evidence.get('file_count', '?')}",
        f"#   families        : {_fmt_families(evidence.get('families', {}))}",
        f"#   encoding        : {_fmt_enc(evidence.get('sample_encodings', {}))}",
        f"#   entropy_mean    : {evidence.get('entropy_mean', '?')}",
        f"#   string_density  : {evidence.get('string_density', '?')}",
        f"#   control_tokens  : {evidence.get('has_control_tokens', '?')}",
        f"#   engine_hint     : {engine_hint or 'desconhecido'}",
        "#",
        "# PRÓXIMOS PASSOS:",
        "#   1. Inspecionar um arquivo representativo no HxD/010 Editor",
        "#   2. Localizar a pointer_table e o formato de string",
        "#   3. Adaptar load_table() e iter_string_offsets() abaixo",
        "#   4. Rodar round-trip (obrigatório antes de avançar)",
        "#",
        "",
    ]
    return "\n".join(lines)


def _fmt_families(families: dict) -> str:
    top = list(families.items())[:5]
    return ", ".join(f"{k}({v})" for k, v in top) or "nenhuma"


def _fmt_enc(encs: dict) -> str:
    return ", ".join(f"{k}: {v:.0%}" for k, v in encs.items()) or "desconhecido"


_FALLBACK_SKELETON = '''
import csv
import sys
from pathlib import Path

# TODO: implementar load_table, decode_string, iter_string_offsets
# Ver framework/connectors/_skeleton/extract.py como referência.

def main(project_json: Path, source_override=None):
    raise NotImplementedError("Conector T2 — completar a implementação")

if __name__ == "__main__":
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    main(proj)
'''
