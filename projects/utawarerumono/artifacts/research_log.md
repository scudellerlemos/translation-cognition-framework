# Research Log — Utawarerumono: Mask of Deception

**Status:** reconciled
**human_input:** provided (usuário entregou a Fandom Wiki como fonte — SRC-002)
**Data de reconciliação:** 2026-06-08
**Fronteira de spoiler:** Cap. 12 (cenas 12_01–12_17). Estendida de 11_01–11_02 em 2026-06 (delta cap.12).
Cobre, no nível de INTRODUÇÃO: vida na vila/estalagem, comédia do moinho, e a chegada do grupo do Ukon —
**Ukon** (guerreiro que faz amizade com Haku), **Maroro** (mago erudito cômico), a **Coorte do Ukon**,
os **Gigiri**/**Boro-Gigiri** (monstros venenosos), **Yamato** (nação) e o **Mikado** (soberano). Mais a
cena-tutorial de sonho (figuras 'Woman'/'Man' como 'Mestre'). Pré-reveal de tudo além do cap.12.
**Seções ignoradas intencionalmente (quarentena de spoiler — NÃO incorporar ao KB):**
- **Identidade verdadeira de Ukon** (reveal de arco posterior) — no cap.12 ele é personagem por si só.
- **Identidade pessoal do Mikado** (reveal de fim de jogo) — no cap.12 é só o soberano/título.
- Identidades das figuras de memória ('Woman'/'Man'), natureza do 'awakening process'/enquadramento
  sci-fi, arcos políticos posteriores, finais — todos além da fronteira.
> A Fandom Wiki (SRC-002) é "sopa de spoiler": ao pesquisar o cap.12, os reveals acima APARECERAM nos
> resultados e foram **deliberadamente descartados** do KB. Ver `spoiler_ledger` (filtro temporal).

---

## Fontes Avaliadas

| ID | Fonte | Tipo | Tier | Cobertura de Spoiler | URL/Caminho | Encontrada por | Usada | Notas |
|----|-------|------|------|----------------------|-------------|----------------|-------|-------|
| SRC-001 | corpus-fonte (ScriptEvent.sdat → dialogs.csv) | Corpus | 1 | Só a cena de abertura | local | IA | Sim | Fonte primária; mineração in-corpus |
| SRC-002 | Utawarerumono Wiki (Fandom) | Wiki | 2 | Página do jogo (li só premissa/elenco inicial) | https://utawarerumono.fandom.com/wiki/Utawarerumono:_Mask_of_Deception | Usuário | Sim | 403 ao fetch direto; conteúdo de abertura corroborado via busca. Seções de reveal **não** lidas. |
| SRC-003 | Wikipedia — Utawarerumono (franquia) | Wiki | 2 | Visão geral/dev/publisher | https://en.wikipedia.org/wiki/Utawarerumono | IA | Sim | Dev Aquaplus; publisher EN Atlus/Sega |

> Gestão de spoiler: deliberadamente **não** abri seções da wiki sobre identidades de memória ou
> metaplot — estão muito além da fronteira (cena 1). Decisão alinhada à política do usuário (traduzir
> preservando a ambiguidade).

### Mineração in-corpus (IA — Fase 1A)
- Rótulos de falante genéricos: "Girl" (0x36a0), "Woman" (0x38b1), "Man" (0x3a9f) — nomes não revelados.
- "Uncle" (0x38dd): tratamento afetivo na memória.
- Enquadramento sci-fi em CAPS: "AWAKENING PROCESS", "SYSTEM ERROR", "COMMENCING COUNTDOWN".
- Lacuna proposital: 0x3937 "...your favorite      !" (6 espaços) — preservar.

---

## Conflitos Resolvidos

| Termo | Versão IA | Versão Usuário | Decisão | Razão |
|-------|-----------|---------------|---------|-------|
| Girl = ? | "provável Kuon" (confidence medium) | SRC-002 confirma Kuon (gata que resgata/cuida) | **Kuon** (confidence high) | Tier 2 corrobora a inferência in-corpus |
| Nome do protagonista | "amnésico, sem nome na cena" | SRC-002: Kuon o nomeia **Haku** depois | **Sem nome em 000S**; "Haku" canônico a partir do nomear (cena posterior) | Coerência com a fronteira; reveal do nome é fora desta cena |

### Decisões de localização tomadas (overridable pelo usuário)
- **Rótulos de falante** `Girl/Woman/Man` → **`Garota` / `Mulher` / `Homem`** (são nomes exibidos na caixa de fala; pt-BR legível).
- **"Uncle"** → **"Tio"** (honorífico afetivo; calque de おじちゃん-like).
- **Nomes próprios** (Kuon, Haku): manter romanização oficial EN. Não aparecem em 000S.
- **Figuras de memória (Woman/Man):** traduzir "às cegas", **preservando a ambiguidade** das falas (sem resolver identidade).

---

## Novos termos confirmados in-corpus (cenas 11_01+11_02)

| Termo | Fonte | Handling |
|-------|-------|----------|
| Kuon (nome) | SRC-001 (0x108db) + SRC-002 | manter_original |
| Haku (nome do protagonista) | SRC-001 (0x12668) | manter_original; reveal em 11_02 |
| Tatari (criatura imortal) | SRC-001 (0x111f7) | manter_original |
| aperyu (vestimenta) | SRC-001 (0xee9b) | manter_original |
| Utawarerumono (origem do nome) | SRC-001 (0x1290a) | manter_original (título) |
| Kujyuri / Província de Shishiri | SRC-001 (0x1102c) | manter (topônimos) |

## Gaps de Pesquisa

- **Localização oficial pt-BR:** não consta (franquia tem EN oficial Atlus/Sega; sem pt-BR conhecido).
- **Identidades de 'Woman'/'Man':** UNSOURCED por escolha (spoiler além da fronteira). confidence low.
- **Natureza profunda do Tatari / enquadramento sci-fi:** UNSOURCED (spoiler). Só o que o corpus diz.
