# ADR 0007 — Gestão de prompt: doutrina versionada em git + hash de drift, sem ferramenta externa

**Status:** aceito · **Data:** 2026-08-30

## Contexto

`PROMPTS.md` documenta QUAIS técnicas de prompting o framework usa (CoT, role-based, instruction
tuning via `context_pack`, RAG em duas camadas). Faltava registrar COMO o prompt em si é gerido:
onde vive, como é versionado, e como se detecta drift entre doutrina e o pacote enviado ao modelo —
decisão até então implícita no código (`context_pack.py`), nunca formalizada.

## Decisão

Gestão de prompt via três mecanismos, todos já implementados, sem plataforma de prompt-ops externa:

1. **Fonte única e versionada.** A Doutrina (Carta) é um arquivo markdown estático,
   `framework/skills/translation_governance.md`, versionado em git como qualquer código. Não existe
   "biblioteca de prompts" separada nem prompt hardcoded em múltiplos lugares — o `system` prompt
   cacheado e o bloco 1 do `scene_prompt.md` vêm sempre desse arquivo.
2. **Montagem determinística, nunca editada à mão.** O prompt por cena (`scene_prompt.md`) é sempre
   *gerado* por `context_pack.py::render_prompt` a partir da Carta + subconjunto curado da cena
   (glossário, vozes, decisões, TM, KB, spoiler guards). Rodar o mesmo input duas vezes produz saída
   byte-idêntica (ver `context_pack.py` docstring). O operador nunca escreve prompt à mão; só edita as
   FONTES (Carta, glossário, decision_log).
3. **Detecção de drift por hash, não por revisão manual.** Todo `pack.json` carrega `doctrine_hash`
   (SHA1 de Carta + glossary.csv + decision_log.md + tone_analysis.md) e `skills_revision` (SHA1 de
   todos `skills/**/*.md`). Qualquer mudança de doutrina/skills entre duas cenas é auditável comparando
   esses campos no artefato — sem precisar de um registro de versões de prompt à parte.

Versionamento = git (histórico, blame, diff de qualquer mudança de doutrina). Nenhum vendor de
prompt-management (Langfuse, PromptLayer etc.) foi adotado.

## Consequências

- (+) Qualquer prompt enviado ao modelo é reconstrutível e diffável via git; nenhum estado de prompt
  vive fora do repo.
- (+) `doctrine_hash`/`skills_revision` dão detecção de drift de graça — sem banco de versões de prompt.
- (+) Zero dependência/infra nova; custo de manutenção é o mesmo de manter markdown versionado.
- (−) Sem tracking nativo de experimentos (comparar variantes de doutrina por custo/qualidade) — se
  isso virar necessidade real, precisa ser construído à parte.
- (−) Alterar a REDAÇÃO do `scene_prompt.md` hoje exige mexer em `render_prompt` (Python, `L.append`
  linha a linha), não um arquivo de template isolado.

**Nota (2026-08-30):** avaliamos migrar `render_prompt` para Jinja2 e decidimos NÃO migrar. O ganho
de um motor de template é separar conteúdo de lógica para quem edita só a REDAÇÃO sem tocar Python —
e não existe esse segundo papel aqui (o único editor do prompt já edita `render_prompt` em Python,
já versionado em git). Sem esse segundo papel, trocar `L.append` por `{% if %}` não muda
comportamento nem reduz manutenção de forma relevante. Reabrir só se: (a) `render_prompt` crescer
bem além do tamanho atual (~140 linhas), ou (b) alguém não-Python precisar editar a redação do
prompt diretamente.
