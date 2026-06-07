# SKILL 03 — KNOWLEDGE BUILDING

## OBJETIVO
Criar mapa estrutural do domínio narrativo.

---

## ⚠️ REGRA MAIS IMPORTANTE DO PIPELINE

Este passo NÃO pode ser executado sem fonte explícita.

👉 SEM FONTE = EXECUÇÃO BLOQUEADA

---

## 🔴 GATE OBRIGATÓRIO (HARD STOP)

Antes de qualquer análise, verificar:

### Existe fonte definida?

Se NÃO existir:

❌ PARAR EXECUÇÃO IMEDIATAMENTE  
❌ NÃO gerar knowledge base  
❌ NÃO inferir nada  
❌ NÃO continuar pipeline  

---

## 🔵 PERGUNTA OBRIGATÓRIA AO USUÁRIO

Se não houver fonte explícita no prompt, o sistema DEVE perguntar:

> “Qual é a fonte do conhecimento do universo?”
>
> Escolha uma opção:
> - arquivo local (ex: dialogs.csv + lore.md)
> - wiki / site (URL)
> - documentação externa fornecida
>
> ⚠️ Este passo não pode continuar sem fonte.

---

## INPUTS (OBRIGATÓRIOS)

Deve conter pelo menos um:

- dialogs.csv (texto do jogo)
- arquivo de lore fornecido
- wiki / fandom / site externo (URL explícita)

---

## 🚫 REGRA DE BLOQUEIO ABSOLUTO

Se fonte não for fornecida:

- NÃO gerar universe_knowledge_base.md
- NÃO inferir lore
- NÃO preencher lacunas
- NÃO prosseguir para glossário ou próximos steps

---

## TAREFAS (SOMENTE APÓS FONTE DEFINIDA)

### 1. Entidades
Descrever apenas o que está suportado por fonte.

Se não houver evidência:
→ marcar como `UNSOURCED`

---

### 2. Relações
Somente relações explicitamente observadas ou documentadas.

---

### 3. Papel narrativo
Derivado exclusivamente de fonte, nunca inferido livremente.

---

### 4. Contexto de uso
Onde e como aparece nas fontes.

---

## FORMATO POR ENTIDADE

```md
## [Entidade]

**Definição:**
(baseada em fonte)

**Fontes:**
- dialogs.csv: offset XXXX
- wiki: URL

**Relações:**
- A → B (fonte: ...)

**Papel narrativo:**
(apenas descritivo, não interpretativo)

**Contexto de uso:**
(onde aparece)

**Status de confiança:**
high / medium / low / UNSOURCED