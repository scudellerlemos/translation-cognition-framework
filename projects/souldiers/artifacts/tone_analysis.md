# Tone Analysis — Souldiers

## Tom geral do jogo

Souldiers é um metroidvania/RPG de ação com narrativa épico-fantástica de dark fantasy com influências nórdicas e egípcias (Valquírias, Ratatosk, mundo dos mortos). O tom é sério mas não pesado — os temas são vida, morte e redenção sem melodrama excessivo.

O humor é **situacional e de personagem**, não meta ou quebra da quarta parede. Vetores principais: Balof (empolgação hiperbólica), Gruper & Makarel (covardia cômica em dupla), Euder (arrogância de fachada).

**Diretriz de prioridade:** Naturalidade e fluidez de leitura rápida em vez de fidelidade literal pesada. O jogador típico de Souldiers lê os diálogos rapidamente. Sem texto travado ou excessivamente formal onde não cabe.

## Espectro de registros

| Personagem | Registro | Referência PT-BR |
|---|---|---|
| Valquíria | Formal-solene, proclamação | Epos — "Ó bravo guerreiro" |
| Jivan | Formal-misterioso | Assertivo, sem gírias |
| Brigard | Formal-militar seco | Ordens curtas, sem contrações coloquiais |
| Sirfiel | Formal-médio, enciclopédico | Vocabulário mais rico |
| Protagonista | Sem fala | — |
| Euder | Coloquial informal arrogante | Contrações, bravatas |
| Edil | Casual-positivo | Incentivo natural |
| Melian | Casual-militar com impaciência | Informal mas contido |
| NPCs genéricos | Neutro-informal | Sem marcador forte |
| Gruper / Makarel | Pastelão / bate-boca | Exagero dramático |
| Balof | Coloquial hiperbólico | Interjeições, empolgação máxima |
| Gartua | Áspero, direto | Sem cerimônias |

## Perfis de voz

### Valkirie/Valkyrie/Valquíria — `voice_criticality: medium`
- **Registro:** formal-solene, proclamação ritual.
- **Características:** sem contrações; sintaxe formal; fala como decreto ("Ó bravo guerreiro"). Impessoal, grandioso.
- **Red flags:** soar coloquial; usar "você" casual; contrações ("pra", "pro").

### Brigard — `voice_criticality: high`
- **Registro:** formal-militar seco.
- **Características:** frases curtas como ordens; sem floreios; estóico. "Silêncio!" — zero palavras desnecessárias.
- **Red flags:** usar gírias; contrações coloquiais; qualquer sentimentalismo.

### Balof — `voice_criticality: high`
- **Registro:** coloquial informal hiperbólico — principal vetor de humor.
- **Características:** empolgação desproporcional; exclamações frequentes (!!!); alívio exagerado; interjeições brasileiras de espanto.
- **Red flags:** soar contido ou sério; perder a energia; registro formal.

### Euder — `voice_criticality: medium`
- **Registro:** coloquial informal com bravatas.
- **Características:** auto-elogio implícito; contrações coloquiais permitidas; contraste com Brigard.
- **Red flags:** soar humilde ou formal; perder a arrogância simpática.

### Jivan — `voice_criticality: medium`
- **Registro:** formal-misterioso, assertivo.
- **Características:** poucas palavras com peso; sintaxe mais elaborada; sem gírias.
- **Red flags:** soar coloquial; usar contrações.

### Makarel/Gruper — `voice_criticality: medium`
- **Registro:** coloquial pastelão, bate-boca em dupla.
- **Características:** medrosos, briguentos, exagero dramático do medo; interrupções mútuas.
- **Red flags:** soar corajosos ou sérios; perder o tom de pastelão.

### Gartua — `voice_criticality: medium`
- **Registro:** áspero, direto, sem cerimônias.
- **Características:** frases muito curtas; durão; sem rodeios.
- **Red flags:** soar gentil ou prolixo.

### Edil — `voice_criticality: low`
- **Registro:** casual-positivo, incentivador.
- **Características:** tom próximo, "você" natural; expressões de encorajamento.
- **Red flags:** soar frio ou distante.

### Sirfiel — `voice_criticality: low`
- **Registro:** formal-médio, enciclopédico.
- **Características:** vocabulário mais rico que soldados; gentil; curiosa.
- **Red flags:** soar agressiva ou vulgar.

## Convenções de PT-BR

- **"você"** (não "tu") em falas informais a neutras — PT-BR brasileiro padrão
- **Contrações coloquiais** ("pra", "pro") permitidas para Balof, Euder, Makarel/Gruper; proibidas para Valquíria, Brigard, Jivan
- Preservar pontuação expressiva: `...` (reticências), `!!!` múltiplos (Balof)
- **Tokens de timing** (`_100_`, `_300_`, `_500_`): nunca remover, nunca adicionar espaço extra antes/depois
- **Tags TMP** (`<color=CHA>`, `<color=LOC>`): preservar verbatim com o nome interno intacto
- Evitar lusismos: "miúdos", "fixe", "gajo", "rapariga" — usar equivalentes PT-BR
- Evitar anglicismos desnecessários quando existe equivalente natural em PT-BR
