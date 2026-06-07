# MEDIA PROFILE — SÉRIES
## Especialização do framework SDD para séries (multi-episódio)

> **Status:** 🚧 **STUB / PONTO DE EXTENSÃO — NÃO VALIDADO.**
> Séries são, em primeira aproximação, **filmes com continuidade entre episódios e temporadas**.
> Herdam tudo de `films.md` e adicionam a dimensão da continuidade. Preencher e validar quando
> houver um projeto real de série.

---

## HERDA DE `films.md`

Formato de fonte (SRT/ASS), constraint de CPS, ausência de linhas de sistema, segmentação por
cena, **conector típico `subtitle_file`** (um por episódio). Ver `films.md` para esses pontos.

---

## DIFERENÇAS-CHAVE EM RELAÇÃO A FILMES

### 1. Continuidade multi-episódio
O corpus se estende por **vários episódios/temporadas**. Decisões terminológicas e de voz feitas
no episódio 1 precisam valer no episódio 50. Implicações:

- O `glossary.csv` e o `decision_log.md` são **compartilhados entre todos os episódios** da série
- O `tone_analysis.md` (perfis de voz) evolui: personagens podem mudar ao longo das temporadas —
  documentar **arcos de voz**, não só voz estática

Proposta para `project.json`:
```json
"series": {
  "shared_glossary": true,
  "shared_decision_log": true,
  "episodes": [
    { "id": "S01E01", "source": "artifacts/s01e01.srt" },
    { "id": "S01E02", "source": "artifacts/s01e02.srt" }
  ]
}
```

### 2. Gestão de spoiler cross-episódio
A `reveal_timing` agora é ancorada a **episódio**, não a capítulo. Um alias revelado em S03E04 não
pode aparecer nas legendas de S01–S03E03. O Passo 7 (QA) precisa de verificação de spoiler
**cross-episódio**, não só cross-segmento.

### 3. Drift de voz ao longo de temporadas
O risco de drift é maior: traduzir 50 episódios ao longo de meses acumula deriva. O Micro-QA e o
QA final ganham importância. Recomenda-se um **QA de continuidade** por temporada: amostrar a voz
de cada personagem recorrente no início e no fim da temporada e comparar.

### 4. Recorrência de terminologia
Termos que aparecem esporadicamente entre episódios distantes são fáceis de traduzir
inconsistentemente. O QA final deve rodar busca global **sobre todos os episódios**, não só o atual.

---

## O QUE SE MANTÉM IGUAL

- Todo o processo dos passos 1–6c por episódio
- A estrutura de artefatos (por episódio, exceto glossário/decision_log que são compartilhados)

---

## PARA VALIDAR ESTE PERFIL

1. Instanciar uma série real com ≥2 episódios e glossário compartilhado
2. Implementar o spoiler-check e a busca de consistência cross-episódio
3. Definir o QA de continuidade por temporada
4. Promover o status de 🚧 para ✅ e documentar os achados
