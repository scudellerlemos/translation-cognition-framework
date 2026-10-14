# Perfis de Voz — [TÍTULO]
## Template de perfil de voz (consumido pelas skills genéricas)

> No pipeline real, estes perfis são produzidos pelo Passo 1 (Discovery) no `tone_analysis.md`.
> Preencha aqui o que já se sabe da obra como semente/referência.
>
> **Campo-chave:** `voice_criticality` (high / medium / low) — personagens `high` exigem
> auto-revisão de voz em cada linha (Passo 6) e verificação dedicada no Micro-QA (Passo 6b).

> **Formato que o runtime lê:** `voice_cards.json` (que o `kb_gate` exige não-vazio) é extraído **só do `tone_analysis.md`**
> (`state_index.build_voice_cards`), não deste arquivo. Lá, cada perfil precisa de cabeçalho `### Nome — `` `voice_criticality: high` `` e
> bullets logo abaixo (até 6 por card, 240 caracteres cada); aliases separados por `/` no cabeçalho.

---

## [Nome do Personagem]

- **voice_criticality:** high | medium | low
- **Registro:** [tom base — ex: casual seco / formal / caloroso]
- **Características:** [traços que definem a voz]
- **Red flags:** [o que sinaliza que a voz saiu do personagem]

---

## [Outro Personagem]

- **voice_criticality:**
- **Registro:**
- **Características:**
- **Red flags:**

<!-- Repetir uma seção por personagem com voz distinta. Priorizar voice_criticality: high. -->
