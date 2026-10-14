# SKILL 08b — TEXTO DE SISTEMA E RÓTULOS EM IMAGEM
## Menu, ajuda, bestiário (texto) e rótulos desenhados em folha de imagem

> **Quando usar:** `extraction_scope: "completo"` e o jogo tem interface fora do diálogo. Roda depois da KB e antes de
> escalar a tradução de sistema; a parte de imagem roda junto da Skill 08 (reinserção).

---

## OBJETIVO

Traduzir o que não é fala sem quebrar a tela: texto de sistema (limite duro de bytes, rótulo curto) e rótulos que
existem só como pixels numa folha de imagem.

## PARTE 1 — Texto de sistema (vai pela sessão, não pela API)

- Cena de sistema listada em `project.json → system_scenes`; speaker `system`, risco `low` salvo dúvida real.
- Orçamento de bytes é teto duro: não coube → abreviar com ponto (`Def.`, `Pes.`). Rótulo curto de menu sem acento
  quando a fonte do menu não tem; frase e descrição com acento normal (ver `charset_note` do conector).
- Nome de item/arma/habilidade/inimigo segue a decisão do glossário (`keep_names`); mesma palavra do original =
  mesma tradução no lote inteiro (atributos, estados, elementos, comandos).
- Lote por seção do arquivo (`session_lot.py split`), com a lista dos nomes mantidos que aparecem nele.

## PARTE 2 — Rótulos em imagem

1. **Inventário:** cada folha vira uma tabela em `project.json → image_labels` (`[y, x0, x1, original, candidatas…,
   largura_medida]`). O texto da obra fica aí; o script do conector não carrega texto.
2. **Reconhecer a folha pelo conteúdo** (hash da área de rótulos), nunca pelo nome do arquivo: a mesma folha se
   repete em vários arquivos e há variantes. Aplicar por hash; arquivo de folha desconhecida não é tocado.
3. **Compor com as letras da própria folha:** cortar os rótulos originais em letras e montar a palavra nova com
   elas (nenhum pixel do jogo entra no repo). Letra que a folha não tem vem do outro estilo ou é desenhada à mão
   (lista curta e registrada: acentos, letras raras).
4. **Régua antes do desenho:** o jogo recorta cada rótulo num retângulo próprio. Medir a largura no jogo (régua de
   teste instalada e removida na instalação seguinte) para os rótulos longos; onde não mediu, vale a célula até o
   vizinho. Não coube → tenta a próxima candidata; nenhuma coube → o rótulo fica como está.
5. **Escopo do pixel:** só o retângulo de cada rótulo muda; teste prova que o resto da folha é idêntico.

## OUTPUTS

`image_labels` no `project.json`; folhas remontadas pelo conector; teste de "fora dos retângulos nada muda"; lista
de rótulos mantidos em inglês e o motivo (decisão ou letra faltando).

## REGRAS CRÍTICAS

- Nunca versionar imagem/folha do jogo (guard). A tabela de rótulos em texto curto é citação pontual.
- O que não foi visto na tela fica marcado "não visto" até haver print (Skill 08c).
