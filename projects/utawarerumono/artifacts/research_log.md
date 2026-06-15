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

## cap.20 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: Utawarerumono Wiki (Fandom) — paginas Vurai, Gundhurua, Uzurusha, Shinonon + corpus (dialogs cap.20).
Reconciliacao autonoma (fonte autorizada no cap.13). O cap.20 abre o arco da invasao de Uzurusha.
- **Uzurusha**: pais ao NORTE de Yamato; horda/imperio nomade invasor. manter_original. (wiki: "country located north of Yamato")
- **Uzurushan / Uzurushans**: gentilico/soldados de Uzurusha -> 'uzurushano(s)' (adjetivo) ou manter 'Uzurushan' como etnia. Traduzir 'Uzurushan army' -> 'exercito uzurushano'.
- **Gundhurua**: REI de Uzurusha; unificou 100+ tribos nomades num poder militar. MASCULINO ("a man who united over..."; wiki). manter_original.
- **Vurai**: 'a Vanguarda' (the Vanguard); um dos Oito Generais-Pilar de Yamato, um dos mascarados; "a lanca poderosa de Yamato". MASCULINO (wiki). manter_original o nome; traduzir o epiteto 'the Vanguard' -> 'a Vanguarda'. SPOILER PROFUNDO (final boss de MoD / desfecho com Oshtor) = beyond_frontier (quarentena) — NAO antecipar; no cap.20 ele aparece em cena, entao o nome em si nao e leak.
- **Jachdwalt**: espadachim famoso, 'the Mirage Blade' -> 'a Lamina Miragem'; pai adotivo de Shinonon; lutador do lado Uzurusha. MASCULINO (wiki). manter_original o nome.
- **Shinonon**: MENINA, filha adotiva de Jachdwalt; brevemente refem da horda Uzurushan. FEMININO (wiki). manter_original.
- **Entua**: 'Lady Entua'; agente do lado Uzurusha, papel no climax (envenenamento/intriga = beyond_frontier). FEMININO (corpus 'Lady'/'she' + wiki). manter_original.
- **Woshis**: agente/desenhista do lado Uzurusha (corpus: "Woshis sketches on his drawing board" -> MASCULINO); papel no climax = beyond_frontier. manter_original. (wiki grafa "Woshisu"; usar a forma do jogo "Woshis".)
- **Zeguni**: Comandante de Uzurusha (corpus: "Commander Zeguni"; tem 'owlo'/vassalo). MASCULINO. manter_original.
- **Akuruturuka**: termo = 'homem mascarado' / forma do guerreiro mascarado (corpus 20_13: "what are we supposed to call that thing!? Akuruturuka"). manter_original + glosar. Lore profunda (mascaras/Oshtor) = beyond_frontier.
- **Nakwan / Nakwans**: termo de Uzurusha = 'soldados-escravos descartaveis' (definido in-corpus 20: "Nakwans? Expendable slave soldiers"). manter_original + glosar.
- **Maruruha**: nacao/regiao que CAIU para Uzurusha (corpus 20_01: "Maruruha has fallen to Uzurusha"). Local. manter_original.
- **Yamatan / Yamatans**: gentilico de Yamato (ja coberto) -> 'yamato'(invariavel)/'de Yamato'; 'Yamatan army' -> 'exercito de Yamato'. Nao e entidade nova, e forma derivada.
- Declinados (ruido/interjeicao/risada/UI/onomatopeia/frase-capitalizada): Hahaha, Hurry, Yamatans (derivado), Ahhhh, Hyahahahahaha, Khakakakakakaka, Open, Reporting, Vanguard (epiteto de Vurai), Yatanawarabe (guarda; pontual), Combat Tutorial/Glossary (UI), LeftLeg (rig), Mirage Blade (epiteto de Jachdwalt), Spine Winds (fala), "Adviser/Advisers/Beside/Damned/Multiple/Soldier/Messenger ..." (prefixos de rotulo + nome ja coberto).

## cap.21 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: idem cap.20 (mesmo arco Uzurusha). Os recorrentes do cap.21 (Jachdwalt, Uzurushan) JA cobertos no delta cap.20 acima.
- Sem entidade nova bloqueante propria. Baixa confianca (1x, nao bloqueiam; conferir na revisao humana, nao chuto): Hamyana Island (ilha; provavel local), Iceman Project / True Humanity Project (termos de lore sci-fi do arco final — beyond_frontier; manter + glosar quando confirmados), Eep/Guard Mm/Haku Eek (interjeicao+rotulo).

## cap.22 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: Utawarerumono Wiki (Fandom) — paginas Tuskur (Country/Person), Aruruu, Camyu, Hakuowlo + Mask of
Deception (lore sci-fi) + corpus cap.22. **Este e o capitulo do REVEAL sci-fi do final** (a obra se passa
na Terra num futuro distante pos-colapso). Spoilers maiores aparecem EM CENA aqui — os nomes em si nao
sao leak (a revelacao acontece neste cap.), mas as conexoes profundas ficam marcadas beyond_frontier.
- **Tuskur**: (pais) nacao-refugio fundada por Hakuowlo; terra natal de Kuon (ela e princesa de Tuskur).
  (pessoa) a velha boticaria que acolheu Hakuowlo (o pais leva o nome dela). manter_original. (wiki)
- **Aruruu** (apelido **Aru**): personagem do Utawarerumono ORIGINAL; irma cacula de Eruruu; anda com o
  tigre Mukkuru. FEMININO. manter_original. (wiki)
- **Camyu**: 2a princesa de Onkamiyamukai; thaumaturga alada (Onkamiyaryu); amiga de Aruruu. FEMININO.
  manter_original. (wiki)
- **Onkamiyamukai**: teocracia de pacificadores, dominada pelos thaumaturgos alados (Onkamiyaryu). Local/
  nacao. manter_original. (wiki)
- **Chii**: filha do Mikado HUMANO (antes da queda da humanidade); **base genetica da Anju**; virou slime
  (praga Tatari); sobrinha do Haku (flashbacks dele). FEMININO. SPOILER MAIOR; conexao Anju/Haku =
  beyond_frontier. manter_original. (wiki/TVTropes)
- **Amaterasu**: satelite de CONTROLE CLIMATICO; tentaram usar como arma -> tempestades catastroficas que
  selaram o fim da humanidade. Termo sci-fi. manter_original + glosar. (wiki)
- **Earth -> Terra**: revelacao de que o mundo e a Terra num futuro distante. 'Earth' TRADUZ -> 'Terra'.
- **Onvitaikayan**: entidade(s) reverenciadas pelos demi-humanos = a antiga HUMANIDADE (Haku e um dos
  poucos sobreviventes onvitaikayan). manter_original + glosar. beyond_frontier (natureza completa).
- **Neko**: corpus-only (1 cena), provavel apelido/criatura; manter_original por seguranca (nao traduzir
  nome). Conferir na revisao humana.
- **Imperial Cloister**: local de Yamato (corpus cap.22; recinto imperial). Traduzir -> 'Claustro
  Imperial' ('Imperial' ja coberto). Fonte: corpus + convencao de Yamato (wiki).
- Baixa confianca (1x, nao bloqueiam): Hiroshi / Hiroyuki (provaveis nomes de humanos pre-queda do arco
  sci-fi — manter se confirmados), Yaana Mauna, Imperial Palace ('Palacio Imperial'), Aru Hm.
- Declinados (contracao/comum/interjeicao): Young, She'd, C'mon, Hmmm, Hm.

## cap.23 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: Utawarerumono Wiki (Fandom) — paginas Benawi, Kurou + corpus cap.23. Capitulo da invasao de
Yamato a Tuskur (defesa de Benawi). Recorrentes ja cobertos: Munechika, Tuskur, Kuon, Anju, Raiko.
- **Benawi**: Mestre de Guerra (Warmaster) de Tuskur; ex-general (mononofu) de Kenashikourupe, rendeu-se
  a Hakuowlo e passou a servir Tuskur ao lado de Kurou. MASCULINO. Forte senso de dever/defesa do pais.
  manter_original. (wiki: Benawi)
- **Kurou**: braco-direito e general companheiro de Benawi em Tuskur ('Lord Kurou'). MASCULINO.
  manter_original. (wiki: Kurou)
- **Warmaster**: patente militar (Warmaster of Tuskur). Traduzir -> 'Mestre de Guerra'. (wiki)
- Ruido tratado no _STOP (nao-entidade): Bro, Eep, Hmhmhm, Hope, Later, They'd, Welcome, Almighty.
  Baixa confianca / artefato de parse (1x, nao bloqueia): Dekopachi (gag de nome trocado de Dekopompo),
  Assassin Grh / Center Blade (rotulo de engine 'Blade_Center'), Loincloth Force / Mononofu's Warehouse
  (nomes-piada de cena unica; traduzir em contexto).

## cap.30 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: Utawarerumono Wiki (Fandom) + corpus cap.30. Recorrentes ja cobertos: Oshtor, Vurai, Nekone,
Nosuri, Honoka, Woshis, Anju.
- **Yatanawarabe**: patente de servo/agente a servico do Mikado ('one of his Yatanawarabe'). Termo do
  mundo. manter_original. (wiki)
- **Ohn Riyaak** (Ohn-Riyaak): 'the Great Sealing' — grande selo/barreira magica do mundo. Nome proprio.
  manter_original. (wiki)
- Ruido tratado no _STOP: Ngh, Hee, Speak, Follow, Open, Osh, Hahh, True, Wonder. Artefatos de parse
  (1x, nao bloqueiam): 'Anju Shit'/'O Osh'/'Wh Osh'/'Wh Lord Oshtor' (truncacoes de fala), Lounge Mode
  (gag), Goodbadguy (apelido de cena), Yatanawarabe Liveruni (Yatanawarabe + nome).

## cap.31 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: corpus cap.31 (2 cenas). Recorrentes ja cobertos: Haku, Oshtor, Ennakamuy, Vurai, Rulutieh.
- Sem entidade nova bloqueante. 'Run' (6x) = verbo/imperativo ('Run, and never stop running'), nao
  entidade -> _STOP. Baixa confianca (1x): Timanonna ('the sun's flower' — metafora/flor, conferir
  na revisao humana; provavel termo poetico, traduzir em contexto).

## cap.39 — delta de KB (reconciliado IA+wiki, 2026-06-14)
Fonte: corpus cap.39 (DLC/pos-jogo, 4 cenas). Recorrentes ja cobertos: Mikado.
- **Dream Arena**: recurso pos-jogo (arena de batalha desbloqueavel; '{c5}Dream Arena{c-} has been
  added'). UI -> 'Arena dos Sonhos'. (corpus)
- Baixa confianca / nonsense proposital (sonho): Deilnidrah / Suolucidteews / Suoluc (palavras de sonho,
  varias ao contrario: 'Suolucidteews' = 'sweeticulos' invertido; manter como onomatopeia/nonsense).
