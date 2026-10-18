# ADR 0018 — Gravação de estado atômica e append sob trava

**Status:** aceito · **Data:** 2026-10-17

## Contexto

A auditoria de arquitetura de 2026-10-17 mediu que, no Windows, `open('a')` do Python com vários processos perde ou
mistura linhas (1498 válidas e 27 corrompidas de 1800 em 5 processos), e que `write_text` direto num JSON de estado
deixa o arquivo truncado se o processo cai no meio. O `wave` e os subagentes em paralelo escrevem nos mesmos arquivos.

## Decisão

1. `paths.atomic_write(p, texto)`: grava num temporário do mesmo diretório (`fsync`) e troca com `os.replace`;
   no Windows repete por ~1 s se o destino estiver aberto por outro processo. Vale para todo JSON/MD/JSONL regravado inteiro.
2. `paths.append_line(p, linha, stale=None)`: append sob `paths.locked` (lock-file `O_CREAT|O_EXCL`). Quem não pega a
   trava em 30 s recebe `TimeoutError`; log de observabilidade (`events.emit`) só avisa, ledger de custo avisa em `log_api_call`.
3. `locked` ganha `stale` (idade em que a trava é órfã), separado de `timeout`; o ledger usa 5 s como antes.
4. O ledger perde o fallback sem trava. SQLite passa a esperar até 30 s por escrita concorrente; não se adota WAL.

## Consequências

- Perde-se um pouco de throughput por append (trava por linha); medido em ms, sem efeito perceptível na onda.
- `*.lock` e `*.tmp` são transitórios e ficam no `.gitignore`.
- Cobertura da migração: estado de execução, traduções, retrotradução e TM; relatórios regeneráveis (lint, quality_sample,
  spoiler_check, bench, fingerprint) continuam com `write_text`, pois uma queda só pede para rodar de novo.
- Fora do escopo, de propósito: o append de `kb_ratified.csv` no `hitl` (manual, uma pessoa por vez).
- Testes: `test_state_integrity.py`. Reverter = trocar as chamadas de volta para `write_text`/`open('a')`.
