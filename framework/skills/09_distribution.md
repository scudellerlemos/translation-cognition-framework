# SKILL 09 — DISTRIBUTION
## Entregar a tradução ao jogador sem distribuir conteúdo do jogo

> **Quando usar:** após o Passo 08 (round-trip verde, gates fechados). Gera um patcher de um clique que
> aplica **só o delta** sobre a cópia do jogador. Nunca publica binário, roteiro ou arte do jogo.

---

## OBJETIVO

Pacote reprodutível a partir de um commit: deltas bsdiff + `manifest.json` (hashes) + `.exe` único, sem Python
no jogador. Instalar, verificar e desinstalar, tudo conferido por hash.

## INPUTS

- `source_dat/` (originais, read-only) e `output/` (remontados pelo Passo 08)
- `projects/<p>/distribution.json`: `titulo`, `titulo_curto`, `autor`, `idioma`, `exe`, `pasta_glob`, `subpasta`,
  `padrao_arquivos`, `processos` (exes que travam os arquivos), `aviso` (linhas da janela), `icone_recorte`
- Opcional: arte do painel e capa (só entram no pacote/`.exe`, nunca no repo; atenção a direitos da arte)

## PASSOS

1. **Pré-condição:** gates verdes e round-trip íntegro. Sem isso, parar (não há bypass).
2. **Pacote** (de dentro do projeto):
   `python -I ../../framework/distribution/build_package.py distribution.json source_dat output dist <versao> [arte [capa]]`
   Só entram arquivos que existem em `source_dat` e diferem dele; sondas de teste ficam de fora.
3. **Executável:** `python ../../framework/distribution/build_exe.py dist output` (saída em `projects/<projeto>/output/`, ignorada no git;
   nunca dentro de `dist/`, que o PyInstaller embute no próprio `.exe`).
4. **Teste obrigatório**, nesta ordem:
   a. CLI numa **cópia** dos originais: `patcher.py verificar|instalar|desinstalar --jogo <pasta> --pacote dist`;
      instalar é idempotente, desinstalar volta byte a byte, arquivo modificado é recusado sem alterar nada.
   b. Trava de jogo aberto (processo real ou falso com o nome de `processos`).
   c. `.exe` no jogo real; depois, máquina limpa (sem Python) e trajeto do piloto.
5. **Texto da release** com versão, hash do `.exe`, taxa de erro da última amostra de qualidade e **limites
   conhecidos**. Reamostrar a qualidade antes de uma `v1.0.0`.
6. **Publicar** (ação do humano ou com aval explícito): release no GitHub com só o `.exe`; guia/canal da
   comunidade aponta para ela e não hospeda arquivo.

## REGRAS DO PATCHER (não alterar sem teste)

- Só altera arquivo cujo hash bate com o original do manifesto; qualquer outro, recusa e não altera nada.
- Backup `.bak` antes de escrever, criado só de arquivo conferido; falha no meio desfaz tudo.
- Recusa instalar/desinstalar com o jogo aberto.
- Não escreve fora da pasta do jogo e não usa rede.

## NUNCA

- Versionar `dist/`, `.exe`, `.bsdiff`, arte ou ícone (o `content_guard` bloqueia).
- Usar fala do jogo em texto de release, guia ou issue.
- Publicar sem o humano confirmar (conta, release e guia são públicos).

## OUTPUTS

`dist/` (deltas, `manifest.json`, `arte.png`, `icone.ico`) e o `.exe` — fora do repositório.
