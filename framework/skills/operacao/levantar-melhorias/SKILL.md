---
name: levantar-melhorias
description: Ao fim de cada onda de tradução, levanta melhorias para o framework a partir da seção "Melhorias para o framework" do ROADMAP do projeto e dos erros vividos na sessão principal, compara com o que o ROADMAP do projeto já registra e acrescenta só o que é novo.
---

# Levantar melhorias para o framework

Rodar no fim de cada onda, depois de fechada (cenas `verified`, custo sincronizado) e antes do `/clear`. O escopo de cada rodada é a onda que acabou de fechar; o que veio de rodadas anteriores já está na seção. Não altera runtime nem o `docs/ROADMAP.md` do framework: tudo fica no ROADMAP do projeto.

## Passos

1. **Fontes do projeto.** Ler a seção "Melhorias para o framework" do `ROADMAP.md` do projeto. Depois varrer a
   sessão principal (desta onda) (conversa e, se faltar contexto, a transcrição em `~/.claude/projects/<projeto>/*.jsonl`) atrás
   de erro, retrabalho, gate que bloqueou, bypass proposto, bug de medição e pedido do usuário que foi contornado.
   Cada achado vira uma melhoria candidata com a evidência (cena, comando, mensagem de erro; sem fala do jogo).
2. **Investigar.** Para cada candidata, abrir o código/doc envolvido e confirmar a causa raiz e o ponto onde o
   conserto entraria (arquivo e função). Descartar o que for particular do jogo e não do framework.
3. **Comparar** com o que já está escrito na seção "Melhorias para o framework" do `ROADMAP.md` do projeto. Classificar:
   - **já registrada** — cita o item existente; só acrescenta a evidência nova a ele;
   - **parcial** — amplia o item existente;
   - **nova** — vira item novo na seção.
4. **Registrar no `ROADMAP.md` do projeto**, na mesma seção: só o que é novo ou parcial é acrescentado (item novo, ou evidência no item existente), com a linha "levantada em AAAA-MM-DD". Mostrar ao usuário o que entrou e o que já estava.

## Regras

- Não implementar o conserto aqui: só registrar no ROADMAP do projeto. Implementar é decisão separada (PATCH/MINOR/MAJOR e ADR se couber).
- Texto público: sem fala do jogo, sem inventário de risco, sem e-mail pessoal.
- Não duplicar item: na dúvida entre "parcial" e "nova", mostrar os dois itens lado a lado e perguntar.
