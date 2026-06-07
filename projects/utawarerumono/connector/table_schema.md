# Table Schema — Utawarerumono
## ⏳ A PREENCHER quando o binário for analisado

> Formato definido em `framework/connectors/_skeleton/table_schema.md`. Este arquivo é consumido
> por `extract.py` E `reinsert.py` — mantê-lo único e estável garante o round-trip.

---

## SEÇÃO 1 — MAPA DE CARACTERES (byte → caractere)

- **Encoding:** custom (TODO confirmar)
- **Largura:** TODO (fixed-1 / fixed-2 / variable)

```
TODO: byte=char a partir da análise no HxD
```

## SEÇÃO 2 — CONTROL CODES (bytes → token)

Devem bater com `project.json → formatting_tokens`.

```
TODO=  {W75}
TODO=  {W80}
TODO=  {W10}
TODO=  {COLOR}
TODO=  {END}
TODO=  \n
```

## SEÇÃO 3 — TERMINADORES E ESTRUTURA

- **Terminador de string:** TODO
- **Alinhamento:** TODO
- **Base de offset:** TODO

## SEÇÃO 4 — PONTEIROS

- **Localização:** TODO
- **Formato:** TODO (endianness + largura)

## SEÇÃO 5 — COBERTURA DE CHARSET DO ALVO (pt-BR)

```
ã -> TODO (presente? ausente?)
ç -> TODO
õ -> TODO
á é í ó ú â ê ô -> TODO
```

Se houver ausências: registrar decisão (expandir fonte vs transliterar) no `decision_log.md`.
