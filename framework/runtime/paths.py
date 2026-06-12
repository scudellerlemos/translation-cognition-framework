"""paths.py — FONTE UNICA do contrato de paths de artefato (H2).

Antes, os nomes de arquivo load-bearing (`translations_<id>.json`, `run_state.json`,
`api_ledger.jsonl`, `state/translation_memory.jsonl`, ...) estavam espalhados por ~18 call sites
como f-strings. Um typo silencioso (ou um rename num lugar so) quebrava o pipeline sem aviso — e o
contrato so existia tribal/no NAMING.md. Aqui ficam os UNICOS literais; os modulos importam estes
helpers. O `test_paths_contract` fixa as strings exatas: qualquer mudanca acidental falha o teste.

Modulo LEAF de proposito: NAO importa nada do runtime (evita import circular com context_pack/model).
Os helpers per-cena recebem `scene_id` EXPLICITO — o chamador ja o tem via `context_pack.scene_id_of`;
nao derivamos aqui p/ nao duplicar essa logica. Tudo retorna `pathlib.Path` (nunca str).

NB de governanca: estes nomes sao CONGELADOS (caps ja traduzidos dependem deles). Mudar um exige
migracao dos artefatos em disco — nao e refactor livre. Ver NAMING.md (contrato estavel).
"""
from pathlib import Path


def artifacts(root) -> Path:
    return Path(root) / "artifacts"


def scene_dir(root, scene) -> Path:
    return artifacts(root) / scene


def state_dir(root) -> Path:
    return artifacts(root) / "state"


def project_json(root) -> Path:
    return Path(root) / "project.json"


# ---- raiz de artifacts/ (estado de execucao + KB) ----
def run_state(root) -> Path:        return artifacts(root) / "run_state.json"
def ledger(root) -> Path:           return artifacts(root) / "api_ledger.jsonl"
def metrics(root) -> Path:          return artifacts(root) / "metrics.jsonl"
def glossary(root) -> Path:         return artifacts(root) / "glossary.csv"
def entities(root) -> Path:         return artifacts(root) / "entities.csv"
def research_log(root) -> Path:     return artifacts(root) / "research_log.md"
def spoiler_ledger(root) -> Path:   return artifacts(root) / "spoiler_ledger.json"
def tone_analysis(root) -> Path:    return artifacts(root) / "tone_analysis.md"
def decision_log(root) -> Path:     return artifacts(root) / "decision_log.md"
def kb_worklist(root, chap) -> Path:    return artifacts(root) / f"kb_phase_worklist_{chap}.md"


# ---- estado duravel destilado (artifacts/state/) ----
def translation_memory(root) -> Path:   return state_dir(root) / "translation_memory.jsonl"
def voice_cards(root) -> Path:          return state_dir(root) / "voice_cards.json"
def decision_index(root) -> Path:       return state_dir(root) / "decision_index.json"


# ---- por cena (artifacts/<scene>/) ----
def dialogs(root, scene) -> Path:       return scene_dir(root, scene) / "dialogs.csv"
def pack(root, scene) -> Path:          return scene_dir(root, scene) / "pack.json"
def scene_prompt(root, scene) -> Path:  return scene_dir(root, scene) / "scene_prompt.md"


def translations(root, scene, scene_id) -> Path:
    return scene_dir(root, scene) / f"translations_{scene_id}.json"


def translation_plan(root, scene, scene_id) -> Path:
    return scene_dir(root, scene) / f"translation_plan_{scene_id}.json"


def back_translation(root, scene, scene_id) -> Path:
    return scene_dir(root, scene) / f"back_translation_{scene_id}.json"


def back_prompt(root, scene, scene_id) -> Path:
    return scene_dir(root, scene) / f"back_prompt_{scene_id}.md"
