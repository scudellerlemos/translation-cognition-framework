# CONECTOR — síntese agêntica (#108)
## Loop propõe → verifica → refina para engine desconhecida, com round-trip como oráculo

> **Status:** processo definido, ferramental existente reutilizado (não é um motor novo).
> Este documento descreve o LOOP — quem faz o quê e em que ordem. O código determinístico que
> o loop chama já existe e é o mesmo usado no fluxo manual (`discover.py`, `script_generator.py`,
> `coverage_gate.py`, `adversarial_validator.py`, `connector_smoke.py`).

---

## POR QUE ISTO É AGÊNTICO (e o resto do framework não é)

O resto do processo (`framework/skills/`) é cognição sobre **texto** (voz, lore, spoiler) — sem
oráculo automático, por isso sempre passa por ratificação humana em cada passo. Conector novo é
diferente: **round-trip byte-idêntico já é um oráculo automático e binário** (passa ou não passa,
sem ambiguidade de julgamento). É o único ponto do framework onde um loop de "IA propõe, verificação
decide, repete até passar" se justifica sem virar geração não-supervisionada de código.

Mesmo assim, o paradigma de governança não muda: **IA propõe, verificação automática decide, humano
ratifica a estratégia final.** O loop nunca promove sozinho um conector para uso em produção.

---

## QUANDO ISTO RODA

`discover.py <game_dir>` classifica o tier (`framework/connectors/tier_classifier.py`). Só
`unknown_engine` aciona este loop — `known_engine` sempre reusa o `reference_connector` do
registry (`connector_registry.json`), nunca gera nada do zero (`existence_gate()`).

---

## O LOOP

```
1. PROPÕE   script_generator.generate(evidence)              -> extract.py candidato
            script_generator.generate_reinsert(evidence)     -> reinsert.py candidato (MESMO padrão)
            (discover.py <game_dir> --generate-stub <dir> gera o PAR de uma vez)

2. VERIFICA (a) coverage_gate.check(candidato, game_dir)     -> dry-run contra N maiores arquivos
               falha aqui = candidato não cobre o corpus real, sem gastar tempo com round-trip
            (b) adversarial_validator.check(candidato)        -> overfitting/variância/offsets
               sobrepostos — pega candidato que só "decorou" 1 amostra
            (c) connector_smoke.smoke(projeto, roundtrip=True) -> ORÁCULO FINAL: SHA256 do
               round-trip extract→reinsert-sem-mudanças === original

3. REFINA   se (a)/(b)/(c) falhar: o diagnóstico (`problems: [...]`) é preciso o bastante pra guiar
            o próximo ajuste (ex.: "_MIN_STRING_LEN muito baixo, 40% ruído" ou "offset 0x3f2 e 0x401
            se sobrepõem"). Quem refina é a mesma sessão/agente que propôs — edita as constantes de
            CONFIG do candidato (nunca a lógica de round-trip em si) e volta pro passo 2.

TETO: 5 iterações de refino. Estourou sem passar em (c) -> escala pra humano com o histórico
completo de tentativas e diagnósticos (nunca solta um loop infinito, nunca declara sucesso parcial).

SUCESSO: round-trip byte-idêntico (passo 2c) = pronto pra RATIFICAÇÃO HUMANA final (registrar no
`connector_registry.json`, promover extract.py/reinsert.py pra `projects/<título>/connector/`).
O loop NUNCA faz esse registro sozinho.
```

---

## O QUE JÁ EXISTIA vs. O QUE ESTE ISSUE ADICIONOU

| Peça | Status antes do #108 |
|------|----------------------|
| Propõe `extract.py` | ✅ já existia (`script_generator.generate()`, 3 padrões por evidência) |
| Propõe `reinsert.py` | ❌ **não existia** — só `extract.py` era gerado; reinsert sempre 100% manual. Adicionado: `script_generator.generate_reinsert()`, mesmo padrão pareado. |
| Verifica cobertura | ✅ já existia (`coverage_gate.py`) |
| Verifica overfitting | ✅ já existia (`adversarial_validator.py`) |
| Verifica round-trip (oráculo) | ✅ já existia (`connector_smoke.py --roundtrip`) |
| `discover.py --generate-stub` gera o par | ❌ **só gerava extract.py**. Adicionado: gera extract.py + reinsert.py juntos. |
| Loop de refino automatizado | Documentado aqui como PROCESSO (quem faz o quê, teto de iterações) — a mecânica de cada iteração reusa as peças acima, não há motor novo de execução. |

---

## LIMITAÇÕES CONHECIDAS DO CANDIDATO GERADO (MVP)

- `generate_reinsert()` escreve no MESMO espaço de bytes original (sem realocar TOC quando a
  tradução cresce além do espaço disponível) — suficiente pra maioria dos casos, já que
  `byte_budget` limita a tradução upstream. Casos que precisam crescer o arquivo (patch com
  realocação) exigem adaptação manual — o candidato sinaliza isso com erro explícito, nunca
  corrompe bytes vizinhos em silêncio.
- Padrão `token_table`: `BYTE_TO_CHAR`/`CONTROL_MAP` nascem vazios nos dois candidatos
  (extract/reinsert) — quem refina precisa preencher lendo a tabela de caracteres real do jogo
  (mesmo trabalho que já era manual antes; o loop não inventa a tabela).
- Sem candidato real de engine verdadeiramente nova disponível hoje pra validar o loop
  ponta-a-ponta (mesma limitação que o `connector_registry.json` teve com "Mask of Truth", #107)
  — validado até aqui só com fixture sintética (`test_script_generator_reinsert.py`).

---

## CHECKLIST DE CONFORMIDADE DO LOOP

```
□ extract.py e reinsert.py candidatos vêm da MESMA evidência (mesmo padrão escolhido)?
□ Nenhuma iteração de refino pula o passo 2c (round-trip) achando "já deve passar"?
□ Teto de iterações respeitado — sem loop infinito, escala pra humano ao estourar?
□ Ratificação final (registrar no connector_registry.json) é sempre uma ação humana explícita?
```
