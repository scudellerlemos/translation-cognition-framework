"""config.py — constantes de TIER/CUSTO/STATUS do harness (leaf, sem dependencias).

Extraido do model.py (god-module). Fonte unica das defaults de modelo, tuning de custo e enums de
status. `model`/`batch`/`back_translate` importam daqui (re-exportado por `model` p/ compat). Sem deps
de runtime -> nunca causa import circular.

Tambem define os TypedDicts dos contratos de retorno das duas chamadas de IA (translate / back_translate).
Tipar aqui (e nao em model.py) evita import circular: config <- back_translate <- model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict, get_type_hints

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

# SEGMENTACAO de submissao (diferente do _BATCH_CHUNK acima, que fatia LINHAS dentro de 1 requisicao):
# aqui fatiamos quantas requisicoes vao em CADA batch submetido a API. Mesmo motivo do
# `_BACK_CHUNK` em back_translate.py (ver feedback-segment-large-batches) — 1 batch com centenas de
# requisicoes pode parecer travado por horas sem sinal confiavel de progresso; um chunk que trava so
# afeta aquele chunk (a cobertura que faltar cai pra proxima rodada do batch_translate).
_TRANSLATE_SUBMIT_CHUNK = 40

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
# MODELO por tier de retighten (so backend "api"): pareado
# posicionalmente com BUDGET_ESCALATION. tol=1.15 (folga maior, a maioria fecha) vai pro barato; tol=1.0
# (o residuo que nem 1.15 resolveu — sinal real de dificuldade, nao suposicao a priori) escala pro caro.
MODEL_ESCALATION = (MODEL_TRANSLATE_CHEAP, MODEL_BACK)   # ("claude-haiku-4-5", "claude-opus-4-8")

AWAITING = "awaiting"   # o operador/modelo do chat precisa produzir a saida
READY = "ready"         # a saida ja existe
DONE = "done"           # chamada de IA concluida (backend api)

# Governanca do glossario: entradas com updated_date mais antiga que este limite geram aviso de revisao.
GLOSSARY_STALENESS_DAYS = 180


# ---------------------------------------------------------------------------
# Contratos de retorno das duas chamadas de IA — TypedDicts (documentacao
# e suporte a mypy/Pylance). Cada funcao retorna um dos shapes abaixo;
# o campo `status` e o discriminante (AWAITING | READY | DONE).
#
# Nota: o campo `usage` e um dict {'in': int, 'out': int, 'cache_read': int,
# 'cache_write': int} (chave 'in' e palavra reservada Python — nao cabe em
# class-based TypedDict; mantem-se como dict anotado nos docstrings).
# ---------------------------------------------------------------------------

class _TranslateBase(TypedDict):
    """Campos presentes em TODOS os retornos de translate()."""
    status: str    # AWAITING | READY | DONE
    scene_id: str
    n_lines: int


class TranslateReady(_TranslateBase):
    """translate() in-session — traducao ja existe em disco (status=READY)."""
    path: str


class TranslateAwaiting(_TranslateBase):
    """translate() in-session — aguardando producao manual (status=AWAITING)."""
    prompt: str
    expected_output: str


class TranslateDone(_TranslateBase):
    """translate() backend api — chamada concluida (status=DONE)."""
    path: str
    model: str
    usage: dict    # {'in': int, 'out': int, 'cache_read': int, 'cache_write': int}
    reused: int
    novel: int


TranslateResult = TranslateReady | TranslateAwaiting | TranslateDone


class _BackTranslateBase(TypedDict):
    """Campos presentes em TODOS os retornos de back_translate()."""
    status: str    # AWAITING | READY | DONE
    reviewed: int


class BackTranslateReady(_BackTranslateBase):
    """back_translate() in-session — resultado ja existe em disco (status=READY)."""
    path: str


class BackTranslateAwaiting(_BackTranslateBase):
    """back_translate() in-session — aguardando producao manual (status=AWAITING)."""
    prompt: str
    expected_output: str


class BackTranslateDone(_BackTranslateBase):
    """back_translate() concluida: reviewed=0 (sem linhas) ou backend api (status=DONE).
    `path` e None quando reviewed=0 (nenhuma linha de alto risco); str nos demais casos."""
    path: str | None


class BackTranslateDoneApi(BackTranslateDone):
    """back_translate() backend api com chamada de rede realizada."""
    model: str
    usage: dict    # {'in': int, 'out': int, 'cache_read': int, 'cache_write': int}


BackTranslateResult = BackTranslateReady | BackTranslateAwaiting | BackTranslateDone | BackTranslateDoneApi


class _RunSceneBase(TypedDict):
    """Campos presentes em TODOS os retornos de run_scene()."""
    status: str
    scene: str


class RunSceneResult(_RunSceneBase, total=False):
    """Retorno de run_scene(). `status` e `scene` sempre presentes; demais por caminho."""
    high: int
    verified: bool | None
    problems: list
    error: str


@dataclass(frozen=True)
class ConnectorSlot:
    """Entrada no registry de conectores do harness."""
    key: str        # chave em project.json connector.{}
    default: str    # script default (relativo a <projeto>/connector/)


CONNECTOR_REGISTRY: tuple = (
    ConnectorSlot("build_plan_script", "build_plan_chapter.py"),
    ConnectorSlot("verify_script",     "verify_chapter.py"),
)

# A2: todas as chaves válidas em project.json connector.{} — inclui as de script
# (CONNECTOR_REGISTRY) + as de metadados/configuração de cada conector.
# _validate_connector_cfg avisa sobre chaves fora desta allowlist (typo guard).
CONNECTOR_KNOWN_KEYS: frozenset = frozenset({
    # — slots executáveis (harness) —
    "build_plan_script", "verify_script",
    # — metadados de tipo e formato —
    "type", "container_format", "table_schema", "encoding",
    # — scripts de conector (não executados pelo harness, mas declarados no manifesto) —
    "extract_script", "reinsert_script",
    # — estratégia de espaço e patch —
    "space_strategy", "patch_format",
    # — charset —
    "target_charset_supported", "charset_note",
    # — tabela de ponteiros (binários com ponteiro central) —
    "pointer_table",
    # — control codes —
    "control_codes",
    # — localização do DAT/arquivo de jogo (nunca persistido, passado via CLI) —
    "game_dat_dir", "game_dat_dir_note",
    # — rastreabilidade de mapeamento —
    "mapping_status", "mapping_note",
    # — conectores CSV/Unity Addressables (Souldiers) — allowlist nunca cobria este formato,
    # descoberto no onboarding do Souldiers (2026-07-02); ver connector-evolution-vision —
    "engine", "data_dir_env", "data_dir_note", "csv_delimiter", "id_column", "text_column",
    "target_column", "target_column_note", "dialogue_tables", "dep",
})


class ConnectorConfig(TypedDict, total=False):
    """A3: forma esperada de project.json connector.{}. Documentação + suporte a mypy/Pylance.
    Todos os campos são opcionais no TypedDict (total=False); o harness valida 'build_plan_script'
    e 'verify_script' em tempo de execução via CONNECTOR_REGISTRY."""
    type: str                       # "hex_binary" | "sdat" | ...
    container_format: str           # "capcom_dat_toc" | "sdat_v4" | ...
    table_schema: str               # caminho relativo ao schema da tabela de ponteiros
    encoding: str                   # "ascii_with_ctrl_codes" | "utf-8" | ...
    extract_script: str
    reinsert_script: str
    build_plan_script: str          # override do default em CONNECTOR_REGISTRY
    verify_script: str              # override do default em CONNECTOR_REGISTRY
    space_strategy: str             # "reconstrucao_secao" | "truncate" | ...
    patch_format: str               # "full_file" | "delta" | ...
    target_charset_supported: bool
    charset_note: str
    pointer_table: dict
    control_codes: dict
    game_dat_dir: str               # TBD — passado via CLI; nunca persistir aqui
    game_dat_dir_note: str
    mapping_status: str
    mapping_note: str
    engine: str                     # "Unity 2021 (Mono, Addressables 1.x)" | ...
    data_dir_env: str               # nome da env var (ex.: "SOULDIERS_DATA_DIR") — nunca o path
    data_dir_note: str
    csv_delimiter: str              # conectores CSV embutido (Unity Addressables)
    id_column: str
    text_column: str
    target_column: str
    target_column_note: str
    dialogue_tables: list
    dep: str                        # dependência Python do conector (ex.: "UnityPy>=1.9.6")


def validate_connector_types(cfg: dict) -> list:
    """A3/#65: valida o TIPO dos valores em project.json connector.{} contra ConnectorConfig.
    Reusa o TypedDict já existente via introspeccao (get_type_hints) — sem dependencia nova
    (pydantic/jsonschema). Chaves desconhecidas nao sao erro aqui (isso e _validate_connector_cfg
    em run_scene.py, que so avisa). Retorna lista de mensagens de erro; lista vazia = tudo ok."""
    hints = get_type_hints(ConnectorConfig)
    errors = []
    for key, value in cfg.get("connector", {}).items():
        expected = hints.get(key)
        if expected is None:
            continue
        if not isinstance(value, expected):
            errors.append(
                f"connector.{key!r} deveria ser {expected.__name__}, veio "
                f"{type(value).__name__} ({value!r}) — corrija project.json"
            )
    return errors


@dataclass
class RunSceneOptions:
    """Opcoes de orquestracao para run_scene() — alternativa tipada aos 6 keyword-args individuais.

    Uso:  run_scene(root, scene, opts=RunSceneOptions(backend="in-session", defer_back=True))
    Equivale a: run_scene(root, scene, backend="in-session", defer_back=True)
    Se `opts` for passado, sobrescreve todos os kwargs individuais.
    """
    backend: str = "api"
    require_back: bool = False
    do_verify: bool = True
    skip_kb_gate: bool = False
    pretranslated: bool = False
    defer_back: bool = False
    rebuild_index: bool = True
    skip_connector_gate: bool = False
    no_back: bool = False
