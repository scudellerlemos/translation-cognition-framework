# Tone Analysis — The Legend of Heroes: Trails in the Sky 2nd Chapter

## Tom geral do jogo

JRPG episódico de fantasia leve, tom majoritariamente caloroso/otimista com humor cotidiano entre
os companheiros de viagem, pontuado por momentos de tensão (investigação da Ouroboros, mistério do
desaparecimento de Joshua). Ritmo de leitura conversacional — diálogo de grupo de viagem, não prosa
literária. Ver `universe_knowledge_base.md` para papel narrativo de cada personagem.

## Espectro de registros

| Personagem | Registro | Referência PT-BR |
|---|---|---|
| Estelle Bright | coloquial, enérgico | Contrações, exclamações, "você" |
| Joshua Bright | polido, contido | Poucas contrações, fala medida |
| Scherazard Harvey | coloquial, confiante, irônica | Contrações; tom de irmã mais velha |
| Olivier Lenheim | floreado, teatral | Frases longas, auto-elogio, sem economia de palavras |
| Agate Crosner | direto, econômico | Frases curtas, pouco floreio |
| Kloe Rinz | formal-cortês, comedida | Sem gírias; registro de estudante de academia |
| Tita Russell | entusiasmada, técnica | Vocabulário técnico (engenharia) misturado a energia juvenil |
| Zin Vathek | formal, ponderado | Fala de veterano; sintaxe mais robusta que a média do grupo |

## Perfis de voz

<!-- FORMATO OBRIGATÓRIO: ### Nome — `voice_criticality: high|medium|low`         -->
<!-- sem esse inline, state_index.build_voice_cards() retorna 0 cards              -->
<!-- aliases: usar / entre nomes alternativos (ex: "### Valkirie/Valkyrie/Valquíria") -->

### Estelle Bright — `voice_criticality: high`
- **Registro:** coloquial, enérgico, otimista
- **Características:** contrações; exclamações frequentes; "nunca desiste" como traço central — evitar tom resignado mesmo em falas tensas
- **Red flags:** soar formal ou comedida; perder a energia entre falas

### Joshua Bright — `voice_criticality: high`
- **Registro:** polido, contido, observador
- **Características:** poucas contrações; fala medida, raramente efusiva; contraste deliberado com Estelle
- **Red flags:** soar tão informal/exclamativo quanto Estelle

### Scherazard Harvey — `voice_criticality: medium`
- **Registro:** coloquial, confiante, levemente irônica
- **Características:** tom de irmã mais velha/mentora; contrações; humor seco ocasional
- **Red flags:** soar juvenil demais ou excessivamente formal

### Olivier Lenheim — `voice_criticality: medium`
- **Registro:** floreado, teatral, narcisista
- **Características:** frases longas e ornamentadas; auto-elogio explícito; nunca é econômico
- **Red flags:** frases curtas e diretas; falta de auto-referência elogiosa

### Agate Crosner — `voice_criticality: low`
- **Registro:** direto, econômico
- **Características:** frases curtas; pouco floreio; fala de quem age mais do que explica
- **Red flags:** soar prolixo ou floreado

### Kloe Rinz — `voice_criticality: medium`
- **Registro:** formal-cortês, comedida
- **Características:** sem gírias; vocabulário de estudante de academia real; educada mesmo sob pressão
- **Red flags:** soar casual/gírio

### Tita Russell — `voice_criticality: low`
- **Registro:** entusiasmada, técnica
- **Características:** vocabulário técnico (engenharia/canhões orbais) misturado a energia juvenil
- **Red flags:** soar apática ou sem o vocabulário técnico

### Zin Vathek — `voice_criticality: low`
- **Registro:** formal, ponderado
- **Características:** fala de veterano; sintaxe mais robusta que a média do grupo; poucas exclamações
- **Red flags:** soar juvenil ou impulsivo

## Convenções de PT-BR

- **"você"** (não "tu") em falas informais a neutras — PT-BR brasileiro padrão
- Evitar lusismos: "miúdos", "fixe", "gajo", "rapariga"
