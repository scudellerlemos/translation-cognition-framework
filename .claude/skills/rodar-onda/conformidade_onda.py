"""Conformidade de um lote de ondas: python conformidade_onda.py <projeto> <t0_epoch> <modelo_janela> <log> [<log> ...]
Confere, so pelo ledger, run_state e logs, se a janela de cada onda cumpriu o contrato (usado para validar a janela em Haiku).
Sai com 1 se algum item reprova; nao altera nada. Os itens que dependem de juizo (qualidade) continuam com o usuario."""
import json
import re
import sys
from pathlib import Path

# modelo esperado por tipo de subagente: traducao em Haiku (retraducao high/critical em Sonnet), retrotraducao em Opus
ESPERADO = {"scene-translator": {"haiku", "sonnet"}, "general-purpose": {"opus"}}


def _familia(m) -> str:
    """claude-haiku-5-5 -> haiku; <synthetic> (resposta sem modelo) e ignorado."""
    return next((f for f in ("haiku", "sonnet", "opus") if f in (m or "")), "")


BYPASS = re.compile(r"--skip-connector-gate|--skip-kb-gate|--no-back\b")


def conferir(proj: Path, t0: float, modelo: str, logs: list[Path]) -> list[tuple[bool, str]]:
    art = proj / "artifacts"
    led = [json.loads(x) for x in (art / "api_ledger.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    antigas = {r.get("session") for r in led if r.get("t", 0) < t0 and r.get("session")}
    led = [r for r in led if r.get("t", 0) >= t0 and r.get("session") not in antigas]
    sc = json.loads((art / "run_state.json").read_text(encoding="utf-8"))["scenes"]
    novas = [k for k, v in sc.items() if v.get("verified") and v.get("_ts", 0) >= t0]
    res: list[tuple[bool, str]] = []
    textos = [lg.read_text(encoding="utf-8-sig", errors="replace") for lg in logs]
    fim_ok = sum(1 for t in textos if re.search(r"^\W*ONDA_OK", "\n".join(t.strip().splitlines()[-3:]), re.M))
    res.append((fim_ok == len(logs), f"ONDA_OK em {fim_ok} de {len(logs)} logs"))
    res.append((bool(novas), f"{len(novas)} cenas verified no lote"))
    janela = {_familia(r.get("model")) for r in led if not r.get("agent_type")}
    res.append((janela - {""} <= {modelo}, f"modelo da janela: {sorted(m for m in janela if m)} (esperado {modelo})"))
    for tipo, ok in ESPERADO.items():
        usados = {_familia(r.get("model")) for r in led if r.get("agent_type") == tipo}
        res.append((usados - {""} <= ok, f"subagente {tipo}: {sorted(m for m in usados if m) or 'nao usado'} (permitido {sorted(ok)})"))
    sem_tipo = [r for r in led if r.get("attribution") == "agent" and not r.get("agent_type")]
    res.append((not sem_tipo, f"{len(sem_tipo)} linhas de subagente sem tipo"))
    res.append((not any(BYPASS.search(t) for t in textos), "nenhuma flag de bypass nos logs"))
    return res


def main(argv: list[str]) -> int:
    proj, t0, modelo, logs = Path(argv[0]), float(argv[1]), argv[2], [Path(p) for p in argv[3:]]
    res = conferir(proj, t0, modelo, logs)
    print(f"# Conformidade do lote (janela {modelo})")
    for ok, msg in res:
        print(f"- {'OK ' if ok else 'FALHOU'} {msg}")
    return 0 if all(ok for ok, _ in res) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
