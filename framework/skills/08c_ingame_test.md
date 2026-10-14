# SKILL 08c — TESTE DENTRO DO JOGO
## Do print do usuário até a causa raiz

> **Quando usar:** depois de cada instalação (Skill 08) e sempre que um print mostrar algo errado. O agente não captura
> a tela: depende de print do usuário em `artifacts/qa_revisao/teste_ingame/prints/` (fora do git).

---

## OBJETIVO

Transformar "está estranho na tela" em causa raiz verificada, sem tentativa e erro no jogo.

## PROTOCOLO

0. **Instalar:** `python framework/runtime/session_lot.py <projeto> install <output> <source_dat> <pasta DAT do jogo> [--go]` (sem `--go` só lista;
   copia os `.DAT` de `output/` que diferem do original e guarda `<arquivo>.bak` só se não existir e só de arquivo idêntico ao original — por
   isso o `.bak` é o ponto de conferência do passo 3).
1. **Pedir print com contexto:** qual tela, qual save/trecho, qual instalação (arquivos instalados + data). Sem isso
   o print não se liga a um build.
2. **Ler o print contra o dado, não contra a memória** (relato textual do tester em `artifacts/qa_revisao/teste_ingame/relato_tester.csv`:
   `quality_review.py tester <projeto> [relato]` localiza a fala pelo trecho visto e gera CORRIGIR no inbox, determinístico, $0): achar o texto na tela → localizar a fala/rótulo no
   `dialogs.csv`/plano pelo texto em inglês ou pelo offset → comparar o que está na tela com a tradução aprovada.
3. **Classificar o sintoma antes de mexer:**
   - tela ≠ tradução aprovada → o arquivo instalado é outro build (conferir hash/`.bak`) ou o reinsert alterou;
   - tela = tradução aprovada, mas feia → defeito de tradução (largura, quebra, registro) → Skill 06b Parte 2;
   - texto cortado/sobreposto → largura da caixa: medir o segmento visível (`box_width.py <projeto>` mostra o limite e a distribuição do inglês; `pattern_lint.py`/`quality_review.py width` varrem o corpus), não supor;
   - caractere errado/sumido → charset/fonte (Skill 00 passo 4);
   - rótulo em imagem cortado → régua do retângulo (Skill 08b);
   - outra fala aparece → ponteiro/offset deslocado (round-trip e `verify_chapter`).
4. **Reproduzir sem o jogo:** montar o caso mínimo (a fala, o arquivo, o reinsert) e ver o defeito nos bytes antes de
   corrigir. Se não reproduz, a hipótese está errada — voltar ao passo 3, não "corrigir mesmo assim".
5. **Corrigir na causa, uma vez, para todos:** se a causa é de padrão (largura, código, fonte), o conserto vai no
   conector/lint e varre o corpus todo; fala avulsa só quando a causa é a fala. Gravar o teste que falha sem o conserto.
6. **Reinstalar e pedir novo print do mesmo ponto.** Só fecha com o print novo.

## REGRAS CRÍTICAS

- Nunca instalar para "ver se resolveu" sem a hipótese escrita no passo 3.
- Jogo aberto bloqueia arquivo: instalar com o jogo fechado (instalação com gates fechados dispensa novo aval caso a
  caso quando o projeto assim registrou).
- Print de jogo não entra no repo; o que vale é a causa e o teste.
