# Sementes de Terminologia — Utawarerumono: Mask of Deception
## Dados de referência do projeto (alimenta o glossary.csv no Passo 4)

> No pipeline real, o `glossary.csv` (Passo 4) é a fonte de verdade operacional.
> Este arquivo registra as decisões terminológicas conhecidas deste título como
> sementes/exemplos. Cada linha do glossário precisa de um `handling_rule` explícito.

---

## manter_original (usar o termo em inglês/japonês romanizado)

- **Nomes de personagens:** todos
- **Locais inventados**
- **Títulos culturais:** Owlo, Mononofu, Kamunagi
- **Termos de lore:** Akuruka, Tatari, Ohn Riyaak
- **Alimentos inventados**
- **Criaturas inventadas**
- **Mecânicas de unidade:** Rakusharai, Ankuam
- **Moeda:** Sen

## traduzir (usar a forma em pt-BR)

- **UI de jogo:** menus, modos de batalha
- **Títulos políticos/militares:** Eight Pillar Generals → Oito Generais dos Pilares
- **Facções com nome descritivo:** Nosuri's Thieves → Ladrões de Nosuri
- **Elementos descritivos genéricos de locais:** Inn, River, Province

## traduzir_parcial (manter nome próprio, traduzir o descritivo)

- Hakurokaku Inn → Estalagem Hakurokaku
- Omuchakko River → Rio Omuchakko
- Kamunagi of Chains → Kamunagi das Correntes

---

## Formas exatas obrigatórias (consistência de título/facção no QA Final)

Estas formas devem aparecer **exatamente assim**, sem variação:

- "Oito Generais dos Pilares" (não "Oito Generais", não "Os Pilares")
- "Escudos Gêmeos de Yamato" (não "Escudos Gêmeos", não "Twin Shields")
- "Kamunagi das Correntes"
- "Estalagem Hakurokaku" (não "Inn Hakurokaku", não "Hakurokaku Inn")

---

## Fases narrativas (tom por fase — consumido no QA Final, Passo 7)

| Fase | Tom esperado |
|------|--------------|
| Inicial (despertar/floresta) | Curioso, levemente cômico, voz interna casual |
| Hakurokaku | Slice-of-life, comédia de ensemble, leveza doméstica |
| Política | Drama crescente, registro mais formal nas cenas de corte |
| Guerra | Gravidade, heroísmo, perda |
| Revelação | Peso, mitologia, tragédia |
