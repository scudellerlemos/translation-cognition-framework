# MEDIA PROFILE — FILMES
## Especialização do framework SDD para legendagem/dublagem de filmes

> **Status:** 🚧 **STUB / PONTO DE EXTENSÃO — NÃO VALIDADO.**
> O processo genérico (`framework/skills/`) foi projetado para ser agnóstico de mídia, mas só foi
> exercitado com jogos. Este perfil documenta as diferenças conhecidas de filmes. Preencher e
> validar quando houver um projeto real de filme.
>
> **Conector típico:** `subtitle_file` (SRT/ASS) — a definir em `framework/connectors/`. Diferente do
> `hex_binary`, a extração/reinserção é parsing de arquivo de legenda (não há byte-space; a restrição
> é CPS/caracteres por linha). O round-trip continua valendo (parse → serializar === original).

---

## DIFERENÇAS-CHAVE EM RELAÇÃO A JOGOS

### 1. Formato da fonte
Filmes usam **legendas com timestamp**, não strings indexadas por offset:
- **SRT** — índice + janela de tempo (`00:01:23,400 --> 00:01:25,900`) + texto
- **ASS/SSA** — idem + estilos, posicionamento, tags de formatação inline

Proposta para `project.json`:
```json
"source": {
  "file": "artifacts/subtitles.srt",
  "format": "srt",
  "id_column": "index",
  "text_column": "text",
  "timing_column": "timecode"
}
```
O `id_column` passa a ser o índice da legenda; o `timing_column` carrega a janela temporal.

### 2. Restrição dominante: CPS (reading speed), não overflow de caixa
A constraint crítica em legendas é **caracteres por segundo** e caracteres por linha — o
espectador precisa conseguir ler dentro da janela de tempo. Substitui (ou complementa) o
`length_constraints` por % do original:
```json
"subtitle_constraints": {
  "max_cps": 17,
  "max_chars_per_line": 42,
  "max_lines": 2
}
```
**Ponto de extensão:** o Passo 6 (auto-revisão) e o Passo 7 (QA) precisam de uma verificação de
CPS no lugar da verificação de overflow de UI.

### 3. Tokens de formatação
ASS tem tags inline (`{\i1}`, `{\pos(...)}`); SRT tem tags básicas (`<i>`, `<b>`). Entram em
`formatting_tokens` como nos jogos — a regra de preservação é a mesma.

### 4. Sem linhas de sistema
Filmes não têm o conceito de "texto de sistema" (CAPS = log). `system_line_convention: none`.
Em compensação, há **rótulos de falante** e **legendas de elementos sonoros** ([MÚSICA], [risos]).

### 5. Segmentação
Por **cena** ou por bloco de tempo, não por lote fixo de N linhas. O Passo 6 pode segmentar por
marcadores de cena se disponíveis.

### 6. Dublagem (se aplicável) adiciona lip-sync
Se o alvo é dublagem e não legenda, surge a constraint de **sincronia labial** e duração de fala —
muito mais restritiva. Provavelmente exige um media-profile `dubbing` separado.

---

## O QUE SE MANTÉM IGUAL (do processo genérico)

- Discovery, Entity Resolution, Knowledge Building, Glossary — **idênticos**
- Voz por personagem, identidade dupla, gestão de spoiler — **idênticos** (filmes têm tudo isso)
- Decision log, planejamento, suites de teste, Micro-QA, ciclo de correção, QA final — **idênticos**
- A única reescrita real é na camada de **formato de fonte + constraint de comprimento/timing**

---

## PARA VALIDAR ESTE PERFIL

1. Instanciar um projeto de filme real com corpus SRT/ASS
2. Implementar o parsing de timestamp e a verificação de CPS
3. Confirmar que os passos 1–5 rodam sem modificação
4. Ajustar os passos 6/7 para CPS e timing
5. Promover o status de 🚧 para ✅ e documentar os achados
