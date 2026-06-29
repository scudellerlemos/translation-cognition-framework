# Breath of Fire IV — Local (Ollama POC)

> Status: **EM DESENVOLVIMENTO — Fase 1 MVP**
> Objetivo: inferência local a custo zero, arquitetura plugável de backend.

---

## O que é este projeto

POC de inferência local para o pipeline de tradução. Reutiliza o conector,
os dados e as regras do BoF4 (125 cenas, glossário, voice cards) com backend
Ollama em vez da Anthropic API. Custo de API: **$0**.

---

## Hardware alvo

| Componente | Spec |
|---|---|
| CPU | AMD Ryzen 5 5600 (6 cores, 3.7 GHz) |
| GPU | AMD Radeon RX 6650 XT (8 GB VRAM, RDNA2) |
| RAM | 16 GB |
| Backend | Ollama (ROCm no Windows) |
| Modelo | `qwen2.5:14b` Q4_K_M (~8.5 GB — partial GPU offload) |
| Velocidade esperada | ~10–15 tok/s (14B partial) / ~25–40 tok/s (7B full VRAM) |

---

## Objetivos

### Done quando:
- [ ] Uma cena do BoF4 traduzida do zero com `--backend ollama`, sem chamar a Anthropic
- [ ] Structured output (schema JSON) funciona com Qwen2.5-14B
- [ ] Benchmark executado: qualidade local vs baseline Sonnet medida
- [ ] Custo: $0 de API

### Objetivos de qualidade:
- Cobertura de linhas ≥ 95% sem retry manual
- Paridade de token de quebra `\n` igual ao API backend
- Sem blowup patológico (linha curta → centenas de caracteres de ruído)

---

## Stack

```
Ollama (ROCm/Windows)
  └── qwen2.5:14b  Q4_K_M
        ├── partial GPU offload (RX 6650 XT 8GB)
        └── fallback: qwen2.5:7b (full VRAM, ~25-40 tok/s)

Backend plugável:
  framework/runtime/ollama_client.py   ← HTTP client (stdlib, zero deps)
  framework/runtime/model.py           ← _ollama_translate() + elif backend="ollama"
```

---

## Como rodar

### Pré-requisitos
```bash
# 1. Instalar Ollama (Windows)
# https://ollama.com/download

# 2. Baixar o modelo
ollama pull qwen2.5:14b

# 3. Verificar que está rodando
python framework/cli.py ollama status
```

### Benchmark (1 cena, ~15 min com 14B)
```bash
python framework/cli.py bench projects/breath_of_fire_4 AREAD001
# ou direto:
python framework/runtime/bench_local.py projects/breath_of_fire_4 AREAD001 --out bench_AREAD001.json
```

### Tradução completa via run_scene
```bash
python framework/runtime/run_scene.py projects/bof4_local AREAD001 --backend ollama --no-verify
```

---

## Estrutura

```
project.json          ← manifesto (referencia connector/dados do BoF4 via ../breath_of_fire_4/)
artifacts/            ← traduções geradas pelo Ollama (separadas do BoF4 aprovado)
  scenes/             ← translations_<scene_id>.json por cena
```

---

## Próximos passos

1. **Executar benchmark em AREAD001** — primeira cena, mede velocidade e qualidade
2. **Benchmark em 5 cenas** — AREAD001, AREAD004, AREAS001, AREAS010, AREAD075 (inclui casos difíceis)
3. **Medir delta de qualidade vs Sonnet** — cobertura, fitting, registro de voz (Fou-Lu arcaico)
4. **Decidir modelo definitivo** — 14B (melhor qualidade) vs 7B (mais rápido, full VRAM)
5. **Back-translation local** — substituir Opus ($) por Ollama ($0) no caminho de QA
6. **Integrar com translation_software** — usar SQLite como store em vez de flat files

---

## Dívidas técnicas

| Item | Prioridade |
|---|---|
| `retranslate_offsets` com backend ollama (escalonamento de fitting) | P1 |
| `batch_back_translate` local (back-translation via Ollama) | P2 |
| Teste de cobertura para `_ollama_translate` (offline, sem Ollama real) | P2 |
| Configuração de timeout via `project.json` (cenas longas) | P3 |
