# Histórico — Utawarerumono (Translation Cognition Framework)

> Projeto concluído. Registro histórico movido do ROADMAP raiz em 2026-06-20.
> Status final: **JOGO COMPLETO — 16 capítulos, 146 cenas, ~45.100 linhas traduzidas e verificadas.**

---

## Resultado final

| Camada | Status |
|---|---|
| Processo genérico (skills 00–08) | 🟢 maduro (~92/100) |
| Harness de escala (`framework/runtime/`) | 🟢 **em produção** — cena = job stateless O(cena); recuperação por-linha + teto previsível; 125 testes |
| Instância Utawarerumono | 🟢 **JOGO COMPLETO — 16 capítulos, 146 cenas, ~45.100 linhas** traduzidos e verificados (round-trip + back-translation), **validado in-game**; **~R$ 65,9 gastos, R$ 0 desperdiçado** |
| Conector hex_binary | 🟢 formato mapeado; **ponteiros FILE-RELATIVOS**; **relocação INTRA-ARQUIVO + rebuild do Pack**; **transliteração NFD**; **pytest** (16 testes) |

**Pendente (pós-produção):**
- [ ] **Fase 3 — Fechamento:** passe global de consistência de glossário → `reinsert` do jogo inteiro + `pytest` + patch IPS final + gate visual in-game.

---

## Fase A — Fechar o caminho até produção

- [x] **A1. Gate in-game.** ✅ pt-BR renderiza no jogo real. EOF-append reprovado (virava `@@@@`); Plano B validado: relocação intra-arquivo + reescrita do Pack.
- [x] **A2. Ordem offset × ordem narrativa.** ✅ Confirmado em 9 capítulos (77 cenas). Extração determinística em ordem de armazenamento = ordem narrativa.
- [x] **A3. Jogo inteiro (~45k linhas).** ✅ 16 capítulos (146 cenas) traduzidos e verificados pelo harness incremental/resumível. Fase 3 (fechamento) pendente.
- [x] **A4. Estimativa de custo real.** ✅ R$/1k linhas 3,12 (forte) → 1,75 (model-mix + caching).
- [x] **A5. Redução de custo.** ✅ Gasto real caps 11–19: ~R$ 43,5, R$ 0 desperdiçado. Alavancas: tiering de modelo, batching (−50%), dedup TM, teto de gasto por driver.

---

## Backlog de qualidade (casos vistos in-game — todos resolvidos)

- [x] **Stammers/hesitações residuais.** ✅ `naturalness_lint.py` varre planos por cena; 0 stammer residual nos caps 11–19.
- [x] **Interjeições EN copiadas cruas.** ✅ 168 substituições aplicadas (Gah→Ai, Urgh→Argh, etc.); `copia_crua`: 266 → 107.
- [x] **Rótulo de falante "Girl" em inglês.** ✅ Opcode `53 00` indexado; 17/17 sites leem "Garota".
- [x] **Carta de Governança de Tradução.** ✅ `translation_governance.md` — contrato de qualidade referenciado pelos gates 06/06b/07.
- [x] **Linter determinístico de naturalidade.** ✅ `naturalness_lint.py` — 12 testes pytest, varre planos por cena.

---

## Já concluído

- ✅ Framework SDD genérico (camadas: processo / perfil / conector / instância).
- ✅ Conector hex_binary completo: container `.sdat`, ponteiros FILE-RELATIVOS, relocação intra-arquivo, transliteração NFD, round-trip byte-idêntico.
- ✅ Primeiro pt-BR do framework renderizado no jogo real (Steam).
- ✅ Harness de escala: 146 cenas, 16 capítulos; stateless, resumível, custo previsível.
- ✅ Governança ponta-a-ponta: round-trip + back-translation + KB + spoiler gates aplicados em volume real.
- ✅ Validation leve: `validate.py` genérico, 7 testes pytest.
- ✅ QA de naturalidade + interjeições localizadas.
- ✅ Charset: transliteração NFD na gravação.
- ✅ Glossário cross-capítulo: linter determinístico (`glossary_lint`), 96 candidatos de nome próprio.
