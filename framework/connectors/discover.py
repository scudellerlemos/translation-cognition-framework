"""
discover.py — CLI do Generic Connector System.

Detecta automaticamente o engine de um diretório de jogo e orienta o próximo passo.

Uso:
    python framework/connectors/discover.py <game_dir>
    python framework/connectors/discover.py <game_dir> --json
    python framework/connectors/discover.py <game_dir> --generate-stub <output_dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from evidence_collector import collect
from tier_classifier import existence_gate, load_registry


def run(game_dir: Path, as_json: bool = False, generate_stub: Path | None = None) -> int:
    """Executa a descoberta. Retorna exit code (0 = engine tratável, conhecida ou não; 1 = bloqueado; 2 = erro)."""
    if not game_dir.is_dir():
        print(f"ERRO: diretório não encontrado: {game_dir}", file=sys.stderr)
        return 2

    print(f"Coletando evidências em: {game_dir}", file=sys.stderr)
    evidence = collect(game_dir)

    if evidence.get("error"):
        print(f"ERRO: {evidence['error']}", file=sys.stderr)
        return 2

    registry = load_registry()
    # Gate de existencia: existence_gate() formaliza que SO engine desconhecida aciona geracao
    # (must_generate); engine conhecida e bloqueado NUNCA chamam script_generator, estruturalmente.
    result = existence_gate(evidence, registry)
    result["evidence_summary"] = {
        "file_count": evidence["file_count"],
        "top_families": dict(list(evidence["families"].items())[:5]),
        "encoding": evidence["sample_encodings"],
        "entropy_mean": evidence["entropy_mean"],
        "string_density": evidence["string_density"],
        "has_control_tokens": evidence["has_control_tokens"],
    }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["tier"] != "blocked" else 1

    _print_report(result, game_dir, registry)

    if generate_stub and result["must_generate"]:
        from script_generator import generate
        stub = generate(evidence)
        out = Path(generate_stub) / "extract.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(stub, encoding="utf-8")
        print(f"\nStub gerado em: {out}")

    return 0 if result["tier"] != "blocked" else 1


def _print_report(result: dict, game_dir: Path, registry: list[dict]) -> None:
    tier = result["tier"]
    print(f"\n{'=' * 60}")
    print(f"  RESULTADO: Tier {tier}")
    print(f"{'=' * 60}")

    if tier == "known_engine":
        engine_id = result["engine_id"]
        engine = next((e for e in registry if e["id"] == engine_id), {})
        print(f"  Engine: {engine.get('name', engine_id)}")
        print(f"  Confiança: {result['confidence']:.0%}")
        print("\n  Evidências:")
        for r in result["reasons"]:
            print(f"    • {r}")
        ref = engine.get("reference_connector", "")
        print("\n  PRÓXIMO PASSO:")
        print("    Copiar o conector de referência:")
        print(f"    {ref}/")
        print("    → projects/<seu-jogo>/connector/")
        print("\n    Depois: pytest connector/test_roundtrip.py --dat-dir <game_dir>")
        print("    (round-trip obrigatório antes de qualquer tradução)")

    elif tier == "unknown_engine":
        print("  Engine: desconhecida — requer implementação manual")
        print("\n  Evidências:")
        ev = result.get("evidence_summary", {})
        print(f"    • {ev.get('file_count', '?')} arquivos encontrados")
        for fam, cnt in (ev.get("top_families") or {}).items():
            print(f"    • {fam}: {cnt} arquivos")
        enc = ev.get("encoding", {})
        if enc:
            print(f"    • encoding: {', '.join(f'{k}: {v:.0%}' for k, v in enc.items())}")
        print("\n  PRÓXIMOS PASSOS:")
        print("    1. Inspecionar arquivo representativo no HxD/010 Editor")
        print("    2. Gerar stub pré-preenchido (padrão escolhido pelas evidências):")
        print("         python discover.py <game_dir> --generate-stub projects/<jogo>/connector/")
        print("    3. Preencher as constantes de CONFIG no stub gerado")
        print("    4. Dry-run OBRIGATÓRIO de cobertura — pega overfitting a 1 amostra ANTES")
        print("       de gastar tempo no round-trip completo:")
        print("         python framework/connectors/coverage_gate.py <candidato.py> <game_dir>")
        print("    5. Validar cada iteração com o smoke test (exit 0 = invariantes OK):")
        print("         python framework/connectors/connector_smoke.py projects/<jogo> [game_dir]")
        print("    6. Quando extract OK: implementar reinsert.py e testar round-trip:")
        print("         python framework/connectors/connector_smoke.py projects/<jogo> [game_dir] --roundtrip")
        print("    7. Round-trip byte-idêntico = conector aprovado → registrar no registry")

    elif tier == "blocked":
        print("  Bloqueado: dados cifrados ou comprimidos")
        print("\n  Evidências:")
        for r in result["reasons"]:
            print(f"    • {r}")
        print("\n  Este engine requer engenharia reversa — fora do escopo do framework.")

    print("\n  Resumo das evidências:")
    ev = result.get("evidence_summary", {})
    print(f"    arquivos: {ev.get('file_count', '?')}")
    print(f"    entropia: {ev.get('entropy_mean', '?'):.2f} bits/byte")
    print(f"    densidade texto: {ev.get('string_density', '?'):.1%}")
    print(f"{'=' * 60}\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if not args:
        print("Uso: python discover.py <game_dir> [--json] [--generate-stub <output_dir>]")
        sys.exit(1)

    game_dir = Path(args[0])
    as_json = "--json" in flags
    stub_dir = None
    if "--generate-stub" in flags:
        idx = sys.argv.index("--generate-stub")
        stub_dir = Path(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else None

    sys.exit(run(game_dir, as_json=as_json, generate_stub=stub_dir))


if __name__ == "__main__":
    main()
