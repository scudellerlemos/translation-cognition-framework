# Revisão humana de qualidade (QA)

Duas pastas:

- **para_revisar/** — o sistema DISPONIBILIZA aqui o `review_*.xlsx` (gerado SEMPRE ao fim de cada
  capítulo, obrigatório). Abra, filtre a coluna "Revisar (onde olhar)", preencha "Correção" (texto certo)
  ou "Nota" (instrução p/ IA) nas linhas erradas. Linha em branco = aprovada.
- **devolvido/** — coloque aqui o arquivo preenchido. Rode:
  `python framework/runtime/quality_review.py apply <projeto>`
  (lê o inbox; processa SÓ as linhas marcadas — verbatim $0 ou nota = IA cirúrgica por linha).
