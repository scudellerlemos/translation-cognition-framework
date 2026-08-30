# Translation Local — Inferência local (Ollama POC; piloto: BoF4)

> Status: **DESCONTINUADO** (2026-08-30) — ver `framework/docs/adr/0008-ollama-local-tier-not-adopted.md`

---

## Por que descontinuado

POC de tier Ollama local (qwen2.5:14b) pra tradução, validado com dados reais nesta sessão:
- **Velocidade:** medida 2,2–3,5 tok/s, 2–4x abaixo do esperado (~10–15 tok/s) — regressão não
  investigada (driver/hardware).
- **Qualidade:** amostra pequena (n=4, `trails_sky_sc/manual_tests/`) já mostrou 1 erro real de
  terminologia ("Aeroliner" — não é palavra em português — vs. "dirigível" no baseline aprovado).

O código do backend (`model.py::_ollama_translate`, `--backend ollama`, `bench_local.py`) foi
removido do framework. `ollama_client.py` continua no repo — é dependência ativa de
`kb_build_ollama.py` (extração de KB, feature separada, não afetada por esta descontinuação).

**Reabrir se:** causa da regressão de velocidade for corrigida, ou surgir necessidade real de
tradução 100% offline que justifique nova validação com amostra maior.
