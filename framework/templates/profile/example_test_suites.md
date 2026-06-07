# Suites de Teste Sintético — [TÍTULO]
## Template (instancia o Passo 5b genérico)

> O Passo 5b genérico descreve **como gerar** suites a partir dos pares de identidade e perfis de
> voz `voice_criticality: high`. Preencha aqui as suites concretas da obra.
> No pipeline real, viram `synthetic_test_corpus.json`.

---

## SUITE-[PROTAGONISTA]-CALIBRATION
Calibra a voz base do protagonista/narrador.

```json
{
  "id": "TEST-001",
  "suite": "SUITE-[PROTAGONISTA]-CALIBRATION",
  "purpose": "[o que valida]",
  "speaker": "[protagonista]",
  "context": "[situação]",
  "text_source": "[linha sintética no idioma-fonte]",
  "expected_register": "[registro]",
  "expected_characteristics": ["...", "..."],
  "red_flags": ["...", "..."],
  "pass_criteria": "[critério de aprovação]",
  "fail_criteria": "[critério de falha]"
}
```

<!--
Gerar uma suite para cada:
- Protagonista/narrador (calibração)
- Par de identidade dupla (distinção — incluir casos de AMBAS as personas)
- Personagem voice_criticality: high (voz dedicada)
- Entidade-ameaça pré-reveal
- Momento de reveal (impacto)

Mínimo de 3 casos por suite.
-->
