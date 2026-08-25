# Universe Knowledge Base — The Legend of Heroes: Trails in the Sky 2nd Chapter

> Síntese da Fase 2 (skill 03), a partir do `research_log.md` reconciliado (SRC-001/002/006).
> Cobertura: personagens jogáveis principais (100%, `importance: main`) + entidades secundárias de
> alta frequência no corpus + facções/lugares centrais. Não é uma wiki completa — cobertura
> narrativa mínima para localização, aprofundada por `kb_phase.py` conforme cenas reais forem
> traduzidas (ver Gaps de Pesquisa no `research_log.md`).

---

## Estelle Bright

**Definição:**
Protagonista e narradora, bracer sênior do Reino de Liberl. Descrita como enérgica, otimista e
persistente — "nunca desiste, não importa a situação".

**Fontes:**
- SRC-002: bio oficial de divulgação do remake
- SRC-006: personagem principal de FC e SC no jogo original

**Relações:**
- Irmã adotiva de Joshua Bright (fonte: SRC-002)
- Filha de Cassius Bright (fonte: SRC-006)

**Papel narrativo:**
No início do jogo, parte em busca de Joshua, que desapareceu.

**Contexto de uso:**
Nome de altíssima frequência no corpus (648 ocorrências em `dialogs.csv`) — protagonista e provável
narradora de boa parte das linhas.

**Status de confiança:** high

---

## Joshua Bright

**Definição:**
Deuteragonista, adotado pela família Bright cinco anos antes do início da história. Cabelo preto e
olhos âmbar. Desapareceu após revelar sua "verdadeira identidade" no Festival de Aniversário da
Rainha — evento que é a premissa de abertura do jogo, não um spoiler de progresso. Backstory real
(Tragédia de Hamel, Stigma implantado por Weissmann) **pesquisada (SRC-007) e quarentenada** em
`spoiler_ledger.json` (entradas `joshua_stigma` e `hamel_tragedy_truth`).

**Fontes:**
- SRC-002: bio oficial de divulgação do remake
- SRC-007 (backstory/Stigma, ver `spoiler_ledger.json`)

**Relações:**
- Irmão adotivo de Estelle Bright (fonte: SRC-002)

**Papel narrativo:**
Objetivo da busca de Estelle no início da história.

**Contexto de uso:**
298 ocorrências no corpus.

**Status de confiança:** high

---

## Scherazard Harvey

**Definição:**
Bracer sênior A-rank, conhecida como "Silver Streak" ("Traço Prateado"). Luta com chicote e artes
orbais. Mentora de Estelle e Joshua; figura de irmã mais velha confiável e carinhosa; gosta de
bebida alcoólica.

**Fontes:**
- SRC-002: bio oficial de divulgação do remake
- SRC-006: mentora dos bracers juniores no jogo original

**Relações:**
- Mentora de Estelle Bright e Joshua Bright (fonte: SRC-006)

**Papel narrativo:**
Figura de orientação/mentoria para os protagonistas.

**Contexto de uso:**
Aparece no corpus como "Schera" (alias, 144 ocorrências) — forma abreviada usada em diálogo casual.

**Status de confiança:** high

---

## Olivier Lenheim

**Definição:**
Músico viajante do poderoso Império de Erebônia, habilidoso em piano, alaúde e pistola orbal.
Personalidade "extremamente narcisista".

**Fontes:**
- SRC-002: bio oficial de divulgação do remake

**Papel narrativo:**
Aliado/companheiro de viagem introduzido no início da jornada.

**Contexto de uso:**
113 ocorrências no corpus.

**Status de confiança:** high

---

## Agate Crosner

**Definição:**
Bracer sênior chamado "Heavy Blade" ("Lâmina Pesada"), domina inimigos com sua espadona (greatsword).

**Fontes:**
- SRC-002: bio oficial de divulgação do remake

**Papel narrativo:**
Bracer sênior encontrado durante a jornada.

**Contexto de uso:**
117 ocorrências no corpus.

**Status de confiança:** high

---

## Kloe Rinz

**Definição:**
Estudante equilibrada/ponderada ("levelheaded") da prestigiada Academia Real Jenis, proficiente com
rapieira e artes orbais.

**Fontes:**
- SRC-002: bio oficial de divulgação do remake

**Papel narrativo:**
Aliada estudante encontrada durante a jornada.

**Contexto de uso:**
113 ocorrências no corpus.

**Status de confiança:** high

---

## Tita Russell

**Definição:**
Neta do "gênio" Professor Russell; aprendiz na ZCF (Zeiss Central Factory), constrói canhões orbais.

**Fontes:**
- SRC-002: bio oficial de divulgação do remake

**Relações:**
- Neta do Professor Russell (fonte: SRC-002)

**Papel narrativo:**
Aliada jovem/técnica encontrada durante a jornada.

**Contexto de uso:**
79 ocorrências no corpus.

**Status de confiança:** high

---

## Zin Vathek

**Definição:**
Bracer veterano imponente, natural da República de Calvard, treinado na escola de artes marciais
Taito.

**Fontes:**
- SRC-002: bio oficial de divulgação do remake

**Papel narrativo:**
Bracer veterano/mentor de combate encontrado durante a jornada.

**Contexto de uso:**
53 ocorrências no corpus.

**Status de confiança:** high

---

## Cassius Bright

**Definição:**
Pai adotivo de Estelle e Joshua. Comandante lendário do Royal Army of Liberl, famoso por repelir o
Exército Imperial na Guerra dos Cem Dias 14 anos antes. Mestre da escola Eight Leaves One Blade.
Retirou-se do exército após perder a esposa na guerra, escolhendo ajudar as pessoas como bracer —
promovido a bracer S-rank por seus feitos.

**Fontes:**
- SRC-006 (Kiseki Wiki, jogo original)

**Relações:**
- Pai adotivo de Estelle Bright e Joshua Bright (fonte: SRC-006)

**Papel narrativo:**
Figura paterna/mentora à distância; comandante lendário do Royal Army.

**Contexto de uso:**
53 ocorrências no corpus (ex.: "My dad, Cassius Bright, went out on a bracer...").

**Status de confiança:** medium (secundário; sourced só pelo SRC-006, sem corroboração de imprensa)

---

## Renne

**Definição:**
Garota do Estado de Crossbell, precoce mas caprichosa, personalidade travessa (descrição oficial de
divulgação). Ligada à investigação da Ouroboros — Estelle e Joshua planejam encontrá-la logo no
início da história. Backstory e natureza completa **pesquisadas (SRC-007) e quarentenadas** em
`spoiler_ledger.json` (entrada `renne_true_nature`, `reveal: beyond_frontier`) — não expandidas
aqui por ser exatamente o mecanismo que o framework usa para separar "o que se sabe" de "o que pode
aparecer na tradução antes do reveal" (mesmo padrão do `utawarerumono`, ver seção Oshtor no KB
daquele projeto).

**Fontes:**
- SRC-004: descrição oficial de divulgação (origem, personalidade)
- SRC-006 (Kiseki Wiki, jogo original) — premissa inicial
- SRC-007 (Kiseki Wiki, sinopse completa) — backstory/reveal, ver `spoiler_ledger.json`

**Papel narrativo:**
Ligada à trama de Ouroboros; ver `spoiler_ledger.json` para o papel completo (quarentenado).

**Contexto de uso:**
81 ocorrências no corpus, em contexto sensível (ex.: "And I couldn't stop Renne, either...").

**Status de confiança:** medium (premissa pública, SRC-004/006) / reveal completo sourced mas
quarentenado (SRC-007, ver ledger) — não inferir natureza/identidade além do que o corpus
já-traduzido ou o guard `pre_reveal` do ledger explicitar.

---

## Anelace Elfead

**Definição:**
Neta do famoso espadachim Yun Ka-fai, especialista na escola Eight Leaves One Blade. Treina junto
com Estelle em Le Locle, campo de treinamento de bracers na região/país de Leman — sede principal da
Bracer Guild.

**Fontes:**
- SRC-006 (Kiseki Wiki, jogo original)
- SRC-007 (Kiseki Wiki, sinopse — Prólogo, uso restrito): localização de Le Locle em Leman

**Relações:**
- Colega de treinamento de Estelle Bright (fonte: SRC-006)

**Papel narrativo:**
Colega bracer / parceira de treino.

**Contexto de uso:**
64 ocorrências no corpus (forma "Anelace").

**Status de confiança:** medium (secundário; sourced só pelo SRC-006)

---

## Kevin Graham

**Definição:**
Sacerdote viajante da Igreja Séptia (Septian Church), percorre o continente lecionando e realizando
ritos em vilarejos pequenos demais para ter igreja própria. Missão real **pesquisada (SRC-007) e
quarentenada** em `spoiler_ledger.json` (entrada `kevin_true_mission`).

**Fontes:**
- SRC-002: personagem jogável novo confirmado no remake
- SRC-006: sacerdote viajante no jogo original, encontra Estelle em viagem de airship a pedido de
  Cassius Bright
- SRC-007 (missão real, ver `spoiler_ledger.json`)

**Relações:**
- A pedido de Cassius Bright, acompanha Estelle em viagem de airship (fonte: SRC-006)

**Papel narrativo:**
Aliado/personagem jogável introduzido durante a jornada.

**Contexto de uso:**
57 ocorrências no corpus.

**Status de confiança:** medium

---

## Liberl

**Definição:**
Reino onde se passa a história; dividido em cinco regiões: Rolent, Bose, Ruan, Zeiss e Grancel
(capital).

**Fontes:**
- SRC-002, SRC-006

**Status de confiança:** high

---

## Rolent / Bose / Ruan / Zeiss / Grancel

**Definição:**
As cinco regiões/cidades de Liberl. Grancel é a capital (sede do Castelo Grancel). Cada uma tem
filial da Bracer Guild.

**Fontes:**
- SRC-006

**Contexto de uso:**
Todos de alta frequência no corpus — Rolent (173x), Ruan (150x), Bose (117x), Grancel (102x),
Zeiss (92x).

**Status de confiança:** high

---

## Bracer Guild

**Definição:**
Organização de bracers (mercenários licenciados que resolvem problemas do cotidiano), com filiais
em todas as cidades principais de Liberl — relação amistosa com o reino.

**Fontes:**
- SRC-006

**Contexto de uso:**
61 ocorrências no corpus.

**Status de confiança:** high

---

## Royal Army of Liberl

**Definição:**
Força militar nacional de Liberl, comandada (no passado) por Cassius Bright.

**Fontes:**
- SRC-006

**Status de confiança:** high

---

## Ouroboros

**Definição:**
Organização/sociedade secreta cujos membros são conhecidos como "Enforcers". Alvo da investigação
que move a trama inicial. Objetivo real ("Plano do Evangelho", liderado por Georg Weissmann, para
obter o Aureole) **pesquisado (SRC-007) e quarentenado** em `spoiler_ledger.json` (entrada
`weissmann_gospel_plan`) — não expandido aqui pelo mesmo motivo da entrada Renne acima.

**Fontes:**
- SRC-006 (existência da organização e o termo "Enforcers")
- SRC-007 (objetivo/mastermind completos, ver `spoiler_ledger.json`)

**Status de confiança:** medium (existência/termo público) / objetivo real sourced mas quarentenado
— não inferir motivações ou membros além do guard `pre_reveal` do ledger.

---

## Leonhardt

**Definição:**
Enforcer nº II da Ouroboros, conhecido como "Bladelord" pela habilidade excepcional com a espada.
No corpus aparece sob o apelido **"Loewe"** — a ligação Loewe = Leonhardt é o twist; papel
narrativo completo **pesquisado (SRC-007) e quarentenado** em `spoiler_ledger.json` (entrada
`loewe_leonhardt`).

**Fontes:**
- SRC-004: bio oficial de divulgação do remake (nome/título públicos)
- SRC-007 (papel narrativo completo/vínculo com Loewe, ver `spoiler_ledger.json`)

**Status de confiança:** medium (bio oficial pública) / papel narrativo sourced mas quarentenado —
ver guard `pre_reveal` do ledger antes de traduzir cenas com "Loewe".

---

## Campanella

**Definição:**
Enforcer nº 0 da Ouroboros, enigmático, com rosto de adolescente e idade real desconhecida.

**Fontes:**
- SRC-004: bio oficial de divulgação do remake

**Status de confiança:** medium (bio oficial de anúncio; papel narrativo não pesquisado)

---

## Aina Holden

**Definição:**
Recepcionista da filial da Bracer Guild em Rolent; segue firme em suas responsabilidades mesmo
preocupada com Estelle e o grupo.

**Fontes:**
- SRC-005 (Gematsu)

**Contexto de uso:**
Personagem de fundo identificada por mineração de frequência no corpus (SRC-001) — gap fechado
nesta rodada.

**Status de confiança:** medium

---

## Jean

**Definição:**
Recepcionista da filial da Bracer Guild em Ruan; animada e simpática.

**Fontes:**
- SRC-005 (Gematsu)

**Status de confiança:** medium

---

## Elnan

**Definição:**
Recepcionista da filial da Bracer Guild em Grancel; gentil e bem-educado.

**Fontes:**
- SRC-005 (Gematsu)

**Status de confiança:** medium

---

## Josette Capua

**Definição:**
Ligada aos "Sky Bandits" (piratas do céu).

**Fontes:**
- SRC-003 (Trails Wiki)

**Status de confiança:** low (citação breve, sem aprofundamento)

---

## Mueller Vander

**Definição:**
Major do Exército Imperial de Erebônia.

**Fontes:**
- SRC-003 (Trails Wiki)

**Status de confiança:** low (citação breve, sem aprofundamento)

---

## Julia Schwarz

**Definição:**
Capitã do exército do Reino de Liberl.

**Fontes:**
- SRC-003 (Trails Wiki)

**Status de confiança:** low (citação breve, sem aprofundamento)

---

## Aidios

**Definição:**
Divindade do mundo do jogo (deusa), referenciada em expressões e invocações dos personagens
(ex.: "What in Aidios'...", "Please, Goddess...").

**Fontes:**
- SRC-006 (mencionada como figura religiosa/mitológica; detalhes não aprofundados)

**Contexto de uso:**
43 ocorrências como "Aidios"; a forma "Goddess" (91 ocorrências) provavelmente se refere à mesma
entidade em boa parte dos casos, mas não confirmado linha a linha.

**Status de confiança:** medium
