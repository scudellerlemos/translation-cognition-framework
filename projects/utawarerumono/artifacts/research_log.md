# Research Log — Utawarerumono: Mask of Deception

**Status:** reconciled
**human_input:** provided (usuário entregou a Fandom Wiki como fonte — SRC-002)
**Data de reconciliação:** 2026-06-08
**Fronteira de spoiler:** Cap. 13 (cenas 13_01–13_09). Estendida do cap.12 em 2026-06 (delta cap.13;
reconciliação corpus cap.13 + Fandom SRC-002). Cobre, no nível de INTRODUÇÃO: tudo do cap.12 + o arco do
cap.13 — **Rulutieh** (princesa de Kujyuri, filha de **Ozen** dos Oito Generais-Pilar; tímida, gosta de
BL), sua ave **Cocopo** (Hororon gigante), os foras-da-lei **Nosuri**/**Ougi**, o criminoso **Moznu**, e —
**reveal ratificado em ch_13_08** — que **Ukon = Oshtor**, o General da Direita / Imperial Guard. Pré-reveal
de tudo além do cap.13. **Twist final de Oshtor (fim de jogo) permanece em quarentena (CRÍTICO).**
**Seções ignoradas intencionalmente (quarentena de spoiler — NÃO incorporar ao KB):**
- **Destino de Oshtor / transferência de máscara** (twist de fim de jogo) — quarentenado (ratificado).
- ~~Identidade verdadeira de Ukon~~ → **revelada em ch_13_08 (Ukon = Oshtor)**; agora dentro da fronteira.
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

## Delta cap.14 (2026-06, reconciliado wiki+corpus)
Fronteira estendida a **14_10**. Novos: Nekone (irma de Oshtor/Ukon), Mikazuchi (Gen. Imperial da Esquerda; disfarce Sakon NAO no corpus 11-14 -> sem ambiguidade no cap.14), Imperial Guard, Twin Shields (Oshtor+Mikazuchi), Mausoleum, Akuruka, + topinimos (Imperial Capital, Omuchakko, Hakurokaku, Onvitaikayan/Great Fathers). Twist Mask of Truth (Nekone encobre Haku) = beyond_frontier, quarentenado. 'Hoo' = risada (interjeicao), nao nome.

## cap.15 — delta de KB (reconciliado IA+wiki, 2026-06-11)
Fonte: Utawarerumono Wiki (Fandom) + corpus do jogo (dialogs cap.15). Reconciliacao autonoma (fonte ja autorizada).
- **Kiwru** (var. Kiuru): principe de Ennakamuy, arqueiro, irmao juramentado de Oshtor/Ukon; MASCULINO; voz nervosa/gentil. Arco romantico (Shinonon) e timeline +10 anos = beyond_frontier → quarentena.
- **Ennakamuy**: nacao dependente de Yamato; terra natal de Kiwru. manter_original.
- **Atuy**: princesa de Shyahoro; FEMININO; lutadora de lanca, busca namorado; informal ('love').
- **Anju**: jovem princesa de Yamato, sucessora do Mikado (a "Descendente Divina"); FEMININO. Origem (template genetico/Chii) = spoiler maior beyond_frontier → quarentena.
- **Divine Scion** → "Descendente Divino/Divina" (concordar com Anju = feminino). Titulo do herdeiro divino do Mikado.
- **Shyahoro**: reino de Atuy. manter_original.
- **Maro**: apelido de Maroro (NAO entidade nova) — `thee call me "Maro!"`; manter consistente com a fala arcaica de Maroro.
- Declinados (ruido/comum, nao-entidade): Papa (=pai, "Papai"), Like, Hold, Help, Yargh, Ahahahaha, e demais interjeicoes/capitalizacao-de-frase.

## cap.16 — delta de KB (reconciliado IA+wiki, 2026-06-11)
Fonte: Utawarerumono Wiki (Fandom) + corpus (dialogs cap.16). Reconciliacao autonoma (fonte autorizada).
- **Yuuri**: personagem feminina, escoltada, timida; admira/imita Karulau; dona do pet Kurarin. manter_original.
- **Kurarin**: pet da Yuuri, agua-viva voadora (pousa na cabeca). MASCULINO. manter_original.
- **Karulau**: figura materna mais velha, forte, retorna da franquia. FEMININO. Lore profunda (idade/Kuon) = beyond_frontier -> quarentena.
- **Rulie**: apelido de Rulutieh (NAO entidade nova).
- Declinados (ruido/comum/interjeicao): Dear, Guess, Ahaha, Getting, Nice, We'd, Agh, Tenant Wheh, Yamatan Soldier Pweeaase, Combat Tutorial (UI), Ladykiller Kurarin (epiteto de Kurarin).

## cap.17 — delta de KB (reconciliado IA+wiki, 2026-06-11)
Fonte: Utawarerumono Wiki (Fandom) + corpus (dialogs cap.17). Reconciliacao autonoma (fonte autorizada).
- **Dekopompo**: Oito Generais-Pilar por sucessao (pai Dikotoma); sem talento militar; MASCULINO; pomposo.
- **Touka**: guarda-costas Evenkuruga (orelhas de falcao), devota mas atrapalhada; FEMININO; retorna da franquia. Lore profunda = beyond_frontier (quarentena).
- **Chalafun**, **Bokoinante** (subordinado do Dekopompo): personagens menores; wiki nao cobre (corpus-only); genero a confirmar no contexto.
- **Nugwisomkami**: termo = 'espiritos/deuses malignos' (lingua do jogo). manter_original + glosa.
- Declinados (ruido/comum/interjeicao/arcaismo): Wait, Cheers, Ooh, Thou, Fate, Game, Perfect, Sisters, Mmmmm, Damn, e fragmentos (Barkeep Welcome, Chalafun Halt, Glad Kuon, etc.).

## cap.18 — delta de KB (reconciliado IA+wiki, 2026-06-11)
Fonte: Utawarerumono Wiki (Fandom) + corpus (dialogs cap.18).
- **Munechika**: Oito Generais-Pilar, 'a Guardia' (escudo/defesa da capital), educadora da Anju; FEMININO; so guerra defensiva.
- **Soyankekur**: Oito Generais-Pilar, owlo de Shyahoro (nacao da Atuy), 'o Marinheiro'; MASCULINO; conheceu Haku pre-mascara.
- **Honoka/Miruhj/Raurau/Mito**: personagens menores (criados/aposentado); wiki nao cobre; corpus-only; genero a confirmar.
- **Highness**->'Alteza' (Anju); **Guardian**->'a Guardia' (epiteto Munechika); **Rulu**->apelido de Rulutieh.
- Os Oito Generais-Pilar (wiki): Raiko, Woshis, Dekopompo, Ozen, Soyankekur, Tokifusa, Munechika, Vurai (alguns aparecerao adiante).
- Declinados (ruido/comum/interjeicao/contracao): Urgh, It'll, Unhand, What're, Nah, Regardless, Understood, Pardon, Oohh, Failure, Pay, Preposterous.

## cap.19 — delta de KB (reconciliado IA+wiki, 2026-06-13)
Fonte: Utawarerumono Wiki (Fandom) + corpus (dialogs cap.19). Reconciliacao autonoma (fonte autorizada).
- **Raiko**: Oito Generais-Pilar, 'o Sabio'; frio e calculista. MASCULINO. Lore profunda (vinculo familiar/arco de antagonista) = beyond_frontier (quarentena; ver spoiler_ledger 'raiko_arc').
- **Shichirya**: escudeiro/servo de Lord Raiko. corpus+wiki; MASCULINO a confirmar.
- **Uruuru & Saraana**: sacerdotisas gemeas (Kamunagi), filhas de Honoka (ja coberta, cap.18; o proprio corpus diz 'daughters of High Priestess Lady Honoka' em 19_05). FEMININO. Uruuru = mais velha, fala curta/informal/girias, pele clara; Saraana = mais nova, fala longa/formal, pele morena. Dadas a Haku p/ servi-lo; magia de agua/fogo + danca.
- **Kamunagi**: titulo de sacerdotisa ('Kamunagi of Chains' -> 'Kamunagi das Correntes'). manter_original + glosa.
- **Magecraft / High Magecraft**: arte magica secreta -> 'Magia' / 'Alta Magia' (traduzir).
- **Nosuri Bandits / Nosuri Thieves**: bando que usa o nome Nosuri (etnia coberta) -> 'Bandidos Nosuri' / 'Ladroes Nosuri' (traduzir o substantivo, manter Nosuri).
- Declinados (ruido/comum/interjeicao/contracao/UI/pontual): Dammit, Sounds, Chains (parte de 'Kamunagi of Chains'), Hahahaha, Hip (hip hooray), It'd, Boys, Forgot, Hear, Kind, Brigand Zzz, Caretaker Ey, Combat Tutorial (UI), Dessert Mountain, Guests Huzzah, Ignoring/Killing Moznu (Moznu coberto), 'Priestess Lady Honoka--her' (Honoka coberta).

## Genero — auditoria de spoiler e resolucao de "a confirmar" (reconciliado IA+wiki, 2026-06-13)
Fonte: Utawarerumono Wiki (Fandom) + corpus. Mata o risco "gender_quarantine inativo": pesquisa em vez de escuro.
- **Gender-spoiler na faixa traduzida (caps 11-19): NENHUM confirmado.** O unico twist de identidade e
  **Haku assumindo a mascara/identidade de Oshtor** — isso e IDENTIDADE (ja coberto no spoiler_ledger
  `oshtor_mask_twist`/`ukon_identity`), nao genero. Logo `gender_quarantine` permanece DORMENTE por estar
  CORRETO (nao ha caso), nao por lacuna. O mecanismo (spoiler_check.check_gender) segue pronto p/ quando
  um caso real surgir (capitulos adiante / outro jogo).
- **Shichirya**: MASCULINO (wiki — tenente de Raiko). Nuance: traveste-se de garota em ocasioes; em cena
  de DISFARCE a traducao deve seguir a apresentacao da cena (nao "corrigir" o genero do disfarce).
- **Honoka**: FEMININO (wiki+corpus cap.19 — Alta Sacerdotisa, mae de Uruuru & Saraana). Resolve o
  "a confirmar" do cap.18 (la aparecia so como criada).
- **Ainda 'a confirmar'** (wiki nao cobre; corpus-only; ficam flagrados no `kb_review --strict` p/
  ratificacao humana, NAO chuto): Miruhj, Raurau, Mito (cap.18); Chalafun, Bokoinante (cap.17).
