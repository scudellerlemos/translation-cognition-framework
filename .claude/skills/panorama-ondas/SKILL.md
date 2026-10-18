---
name: panorama-ondas
description: Mostra o progresso real da tradução (falas e cenas feitas sobre o total do jogo), a ordem dos capítulos (confirmada ou não) e o plano das próximas ondas com antecedência. Usar ao reportar progresso, antes de propor onda ou quando o usuário perguntar quanto falta.
---

# Panorama de falas, ordem e ondas

## Passos

1. Rodar `python .claude/skills/panorama-ondas/panorama.py projects/<nome> [n_ondas]` (padrão: 8 ondas à frente na tela; `0` = todas).
   O script grava sempre o panorama completo, com as 96 ondas, em `artifacts/panorama_ondas.md` (sobrescreve a cada rodada).
   O arquivo só tem ids e números, mas `artifacts/` é default-deny no guard: fica local, não é versionado.
2. Mostrar a saída ao usuário. Todo relato de progresso traz o total do jogo ao lado ("1.880 de 23.633"),
   nunca "recorte completo" sozinho.
3. **Ordem dos capítulos.** Vem do próprio jogo: `python .claude/skills/panorama-ondas/extrai_ordem.py projects/<nome> "<pasta Data>"`
   lê `ENG/DataBase.sdat:EventManagerData.bin` (433 eventos em ordem de jogo) e grava `artifacts/ordem_cenas.txt`
   (um id de cena por linha). Cena que o jogo não lista (sub-cenas disparadas por script) entra logo depois da
   última listada do mesmo `NN_NN` (verificado: 56 das 71 são falas de combate, scripts `B`, da batalha desse evento;
   as 15 sem evento são textos de menu: tutorial `98_98_*`, mensagens de ranking `99_61/62_*` e as falas `00_90_*`). Sem o arquivo, o script usa ordem numérica e avisa "NÃO CONFIRMADA".
4. **Plano.** Ondas de até 6 cenas, ~400 a 700 falas; cena acima de 700 vai sozinha. O plano é sugestão: a onda
   só roda pela skill `rodar-onda`, com o "sim" do usuário no recorte e no custo.

## Notas

- Total = linhas de `dialogs.csv` por cena (23.633); o extrator conta 23.970 strings porque inclui as vazias.
- "Feita" = cena `verified` no `run_state.json` (mesmo critério do `cost_report`).
- Estimativa de custo: ~US$ 0,008 por fala em equivalente API (onda 1 a 6, Sonnet); é extrapolação, não promessa.
- Texto público (ROADMAP, issue, commit): só ids de cena e números, sem fala do jogo.
