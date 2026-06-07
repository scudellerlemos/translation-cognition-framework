# SKILL 04b — DECISION LOG
## Registro de decisões de localização — auditoria do processo

> **Quando usar:** Sempre que uma decisão de localização não-óbvia for tomada, em qualquer passo do SDD. Este arquivo é acumulativo — nunca apagar entradas existentes.

---

## OBJETIVO

Tornar o processo auditável. Quando uma decisão for questionada futuramente ("por que traduzimos X assim?"), a resposta está aqui com o raciocínio completo. Também previne que a mesma discussão aconteça duas vezes.

---

## QUANDO REGISTRAR

Registrar **obrigatoriamente** quando:

- Uma decisão de `handling_rule` no glossário não é óbvia (ex: por que este alimento é tratado como nome próprio?)
- Uma tradução se afasta do `base_translation` do plano por razão específica
- Uma regra geral tem exceção em contexto específico
- Uma linha de alto risco recebe tratamento especial
- Uma decisão é revertida (registrar a reversão + razão)
- Uma dúvida é resolvida após consulta externa (wiki, fanbase, material oficial)

**Não registrar:** decisões triviais e óbvias (manter nome de personagem, traduzir elemento de UI).

---

## ESTRUTURA DO ARQUIVO

```markdown
# Decision Log — [Nome do Projeto]

---

## [TERM ou OFFSET] — [título curto da decisão]

**Data:** YYYY-MM-DD
**Passo do SDD:** [04 / 05 / 06 / 07]
**Tipo:** [handling_rule / tone / spoiler / formatting / revision]

**Decisão tomada:**
[O que foi decidido. 1-2 frases objetivas.]

**Alternativas consideradas:**
- [Alternativa A] — rejeitada porque [razão]
- [Alternativa B] — rejeitada porque [razão]

**Razão da decisão final:**
[Explicação do raciocínio. Pode citar regra do translation_rules.md, precedente externo, ou escolha editorial consciente.]

**Impacto:**
[Onde esta decisão afeta o texto. Quais segmentos são influenciados.]

**Revisão necessária:** [sim / não]
[Se sim: o que precisa ser revisado e quando.]

---
```

---

## EXEMPLO PREENCHIDO

```markdown
## Amamunii / Amam — forma abreviada em diálogo casual

**Data:** 2025-06-07
**Passo do SDD:** 04
**Tipo:** handling_rule

**Decisão tomada:**
"Amam" é aceita como forma abreviada informal de "Amamunii" em diálogo casual entre 
personagens familiarizados. "Amamunii" é a forma completa padrão em todos os outros contextos.

**Alternativas consideradas:**
- Usar sempre "Amamunii" — rejeitada porque elimina a variação de registro que o original tem
- Usar sempre "Amam" — rejeitada porque perde a forma completa que aparece em contextos formais

**Razão da decisão final:**
O original japonês usa variação de forma dependendo do contexto social da fala. 
Replicar isso em pt-BR com Amamunii (formal/narrativa) vs. Amam (casual/diálogo) 
preserva a intenção de caracterização.

**Impacto:**
Afeta qualquer linha de diálogo casual entre Haku e Kuon ou outros personagens 
familiarizados que mencionem o alimento.

**Revisão necessária:** não
```

---

## TIPOS DE DECISÃO

| Tipo | Quando usar |
|------|-------------|
| `handling_rule` | Decisão sobre manter_original / traduzir / traduzir_parcial |
| `tone` | Decisão sobre registro de voz, adaptação de comédia, ritmo |
| `spoiler` | Decisão sobre quando e como tratar alias de spoiler |
| `formatting` | Decisão sobre tokens, pontuação, quebras de linha |
| `revision` | Reversão de decisão anterior — sempre documentar o que mudou e por quê |
| `external` | Decisão baseada em consulta externa (wiki, fandom, material oficial) |

---

## ARQUIVO INICIAL

O arquivo `decision_log.md` no projeto começa com o cabeçalho e uma seção vazia. É preenchido ao longo de todo o projeto.

**Localização:** `decision_log.md` na raiz do projeto (mesmo nível do `glossary.csv`).

---

## REGRAS CRÍTICAS

- **Nunca apagar entradas.** Se uma decisão foi revertida, adicionar nova entrada do tipo `revision` — não editar a entrada original.
- **Registrar no momento da decisão**, não em lote retroativo. Decisões registradas depois perdem o contexto que as motivou.
- O decision log é lido no início de cada sessão de trabalho para garantir que decisões anteriores não sejam refeitas inconscientemente.
- Em caso de dúvida sobre se algo merece registro: registrar. O custo de registrar algo desnecessário é zero; o custo de não registrar algo necessário pode ser alto.
