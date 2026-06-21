# Tone Analysis — Breath of Fire IV

> Status: inicial — derivado do voice_profiles_reference.md e corpus piloto (AREAD001).
> Refinar após análise de cenas completas e sessões de jogabilidade.
> Formato: lido automaticamente por state_index.build_voice_cards() → voice_cards.json.

---

## Personagens principais

### Ryu — `voice_criticality: high`
- Protagonista; jovem caído do céu sem memórias.
- Registro: simples, direto, honesto. Poucas palavras; expressa-se por ação.
- Tom: tranquilo, levemente ingênuo; cresce em determinação ao longo da história.
- Red flags: verbose demais; soar adulto/calculista; resolver dúvidas que o personagem não resolveria.
- Contraste obrigatório com Fou-Lu: mesma entidade, voz completamente oposta.

### Nina — `voice_criticality: high`
- Princesa de Wyndia buscando noivo desaparecido.
- Registro: formal-médio com calor. Liderança discreta; determinada.
- Tom: esperançosa mas realista; forte senso de responsabilidade.
- Red flags: soar fria ou passiva; perder a firmeza que a caracteriza como líder do grupo.

### Cray — `voice_criticality: medium`
- Guerreiro Woren; companheiro de Nina desde a infância.
- Registro: direto, protetor, levemente bruto. Frases curtas; poucas palavras longas.
- Tom: leal, pragmático; afeto por Nina mantido contido.
- Red flags: floreios verbais; soar filosófico; expor emoção abertamente.

### Ursula — `voice_criticality: medium`
- Oficial do Exército Imperial.
- Registro: formal-militar. Ordens curtas. Evolui para tom mais pessoal conforme confia no grupo.
- Tom: rígida no início; gradualmente mais humana.
- Red flags: soar casual desde o início; perder a progressão de confiança.

### Fou-Lu — `voice_criticality: high`
- Primeiro Imperador ressurgido; alter-ego de Ryu.
- Registro: arcaico, solene, majestoso. Pronomes imperiais; vocabulário elevado.
- Tom: distante, poderoso, eventualmente amargo e trágico.
- Red flags: soar casual ou moderno; aproximar o registro do Ryu; resolver a ambiguidade do personagem.
- CRITICAL: voz completamente distinta de Ryu — nunca moderar o arcaísmo.

### Scias — `voice_criticality: medium`
- Mercenário felino (Khán); fala com gaguejo característico.
- Registro: hesitante, com gaguejos, linguagem simples.
- Tom: leal apesar da aparência desleixada; humor involuntário.
- Red flags: perder o gaguejo (é traço identitário central); soar articulado ou fluente.
- Convenção de gaguejo em pt-BR: a definir no decision_log.md após cenas com Scias.

---

## Personagens secundários

### Yuna — `voice_criticality: medium`
- Antagonista principal; cientista imperial; manipulador refinado.
- Registro: educado, preciso, ligeiramente condescendente. Nunca grita; nunca perde a compostura.
- Tom: frio-intelectual; entusiasmo contido ao descrever seus experimentos.
- Red flags: soar raivoso ou passional; perder a polidez superficial que mascara a crueldade.

### Deis — `voice_criticality: medium`
- Deusa aprisionada; tom irônico e levemente superior.
- Registro: sarcástico, irreverente, divertido com a ingenuidade dos mortais.
- Tom: poderosa mas entediada; curiosidade genuína disfarçada de desdém.
- Red flags: soar agressiva; perder o humor sofisticado; tratar personagens com seriedade excessiva.

---

## Categorias especiais

### npc — `voice_criticality: low`
- NPC sem perfil de voz dedicado (personagens secundários, aldeões, guardas, mercadores genéricos).
- Registro: neutro-médio; adaptar ao contexto imediato da cena (hostil, amigável, comercial).
- Tom: sem traço fixo de voz — cada fala é independente do grupo.
- Red flags: impor voz de personagem conhecido; forçar consistência entre npcs de cenas distintas.

### system — `voice_criticality: low`
- Mensagens do sistema de jogo: tutoriais, confirmações de menu, avisos de interface.
- Registro: neutro, impessoal, imperativo quando necessário.
- Tom: informativo; sem personalidade de personagem.
- Red flags: adicionar voz de personagem; usar registro informal.

### unknown — `voice_criticality: low`
- Falante não identificado no corpus: NPCs genéricos, vozes de multidão, textos sem speaker_code.
- Registro: neutro-médio; adaptar ao contexto da cena.
- Tom: sem traço de voz fixo — cada fala é independente.
- Red flags: impor voz específica de personagem conhecido; forçar consistência entre falas de 'unknown'.
