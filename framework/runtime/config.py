"""config.py — constantes de TIER/CUSTO/STATUS do harness (leaf, sem dependencias).

Extraido do model.py (god-module). Fonte unica das defaults de modelo, tuning de custo e enums de
status. `model`/`batch`/`back_translate` importam daqui (re-exportado por `model` p/ compat). Sem deps
de runtime -> nunca causa import circular.
"""
from __future__ import annotations

# --- model-mix (defaults; cost_model cenario 'mix'): Sonnet traduz, Opus verifica alto risco ---
MODEL_TRANSLATE = "claude-sonnet-4-6"
MODEL_BACK = "claude-opus-4-8"
# TIERING por complexidade (so no caminho BATCH): linhas SEM token de quebra (single-line, maioria) vao
# p/ o Haiku (-67%/linha; benchmark: voz no nivel do Sonnet, inclusive registro arcaico); linhas COM `\n`
# (multi-linha) ficam no Sonnet (Haiku derrapa na disciplina de \n em escala — paridade so falha onde HA
# \n, entao o split DRIBLA a fraqueza). O caminho interativo (fallback/escalonamento) fica Sonnet (casos
# dificeis = confiabilidade). MODEL_TRANSLATE_CHEAP=None desliga o tiering (tudo Sonnet no batch).
MODEL_TRANSLATE_CHEAP = "claude-haiku-4-5"
# Amostragem de QUALIDADE do tier barato: a back-translation so cobre high/critical, deixando as
# low/medium (boa parte single-line -> Haiku) SEM crivo de qualidade (round-trip so prova bytes). Uma
# fracao DETERMINISTICA das low/medium entra na back-batch -> piso de qualidade medido p/ o Haiku.
BACK_SAMPLE_RATE = 0.05

# Saida pode ser grande (ate ~500 linhas x speaker/tone/intent/risk/t). Streaming evita timeout;
# este teto cobre a maior cena do corpus com folga (Sonnet/Opus 4.x suportam ate 64k de saida).
MAX_OUTPUT_TOKENS = 64000
# CHUNKING do batch: o endpoint de batch TRUNCA a saida estruturada longa (~100 linhas/resposta,
# DETERMINISTICO — medido no 15_06: 120/221 linhas sempre faltando, identico nas 3 rodadas; re-mandar
# nao adianta, volta o mesmo prefixo). Quebrar a cena em pedacos pequenos faz cada request voltar
# COMPLETO; a cobertura acumula entre os chunks. (O interativo/streaming escapa pq trunca em pontos
# variaveis a cada retry -> a uniao das 3 cobre; o batch trunca igual -> a uniao nao cresce.)
_BATCH_CHUNK = 60     # linhas por requisicao de batch (folga sob o teto ~100 medido)
_MAX_TRIES = 3        # tentativas p/ corrigir saida invalida (cobertura / token de quebra)

# Tuning de custo da TRADUCAO (medido: effort:high + thinking estourou ~5x o cost_model — o thinking
# conta como saida a $15/M). Traducao com contexto curado nao precisa de raciocinio profundo:
# default sem thinking + effort baixo. back_translate (alto risco) mantem thinking (raciocinio importa).
EFFORT_TRANSLATE = "low"
THINK_TRANSLATE = False

# Disciplina de orcamento: a traducao TRANSLITERADA (sem acentos — como vai p/ os bytes) nao deve
# estourar MUITO o byte_budget. E SOFT (best-effort): linhas acima de budget*tol recebem um nudge de
# encurtamento nas retries, mas sao aceitas (o conector absorve crescimento; a VERIFY e o juiz real).
# 1.40 = DEFAULT (alinhado ao build_plan; traducoes naturais, menos retries = mais barato). Cenas de
# binario APERTADO (multi-BIN) podem nao caber a 1.40 -> o run_scene ESCALA o aperto (1.40->1.15->1.0)
# e re-traduz so quando a VERIFY falha por fitting (out-of-file/residuo). Ver BUDGET_ESCALATION.
BUDGET_TOLERANCE = 1.40
BUDGET_ESCALATION = (1.15, 1.0)   # tolerancias mais apertadas tentadas, em ordem, na falha de fitting

AWAITING = "awaiting"   # o operador/modelo do chat precisa produzir a saida
READY = "ready"         # a saida ja existe
DONE = "done"           # chamada de IA concluida (backend api)
