# Revisão humana de qualidade (QA) — dois papéis

> Guia completo do framework (filosofia + gates + papéis): `framework/docs/QA_REVIEW.md`.
> Abaixo, o resumo prático desta instância.

Dois papéis humanos **convergem no mesmo `apply`** (determinístico, $0 de IA salvo a "nota"):

## Papel 1 — REVISOR (lê o texto)
1. Abra **`para_revisar/review_all.xlsx`** (gerado SEMPRE ao fim de cada capítulo, obrigatório).
2. Use as dicas: **"Revisar (onde olhar)"** (micro-QA da IA já pago) e **"Caixa (cresceu vs EN?)"**
   (`ESTOUROU` = quebra quase certa; `rever` = cresceu vs o original; vazio = cabe, provado).
3. Na linha errada, escreva **CORRIGIR** na coluna "Corrigir?" e preencha **uma**:
   - **Correção** = o texto certo → aplicado **verbatim ($0)**;
   - **Nota** = instrução (ex.: "encurtar") → IA reescreve **só aquela linha**.
4. Salve em **`devolvido/`** → `python framework/runtime/quality_review.py apply <projeto>`

## Papel 2 — TESTER (joga o `.sdat`)
Acha problemas na **tela** (balão estourado, texto cortado, termo errado no contexto). Como in-game
não se vê offset, o fluxo é **determinístico, sem OCR/IA** (o print é PROVA, não a fonte do texto):
1. Largue o **print** em `teste_ingame/prints/`.
2. No `teste_ingame/relato_tester.csv`, por linha:
   - **print** = nome do arquivo · **texto_visto** = ~3-5 palavras do pt-BR que apareceu (chave p/
     localizar) · **problema** = balão/quebra/sentido · **sugestao** = (opcional) o texto certo.
3. Rode: `python framework/runtime/quality_review.py tester <projeto>`
   - casa o trecho (acento dobrado = igual ao transliterado da tela) nos aprovados → acha cena+offset;
   - gera linhas **CORRIGIR** em `devolvido/` → entram no **mesmo `apply`**;
   - ambíguos (trecho repetido) / não-achados são listados p/ você desempatar pelo print.

> Prints e o relato preenchido **não vão pro git** (dados do tester); o resultado entra em
> `translations` (versionado). Quem "lê" a tela é o tester — sem IA.
