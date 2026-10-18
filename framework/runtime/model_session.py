"""model_session.py — caminho de SESSAO do translate (ADR 0019): sem rede.

Garante o scene_prompt.md e confere se o agente da sessao ja escreveu translations_<cena>.json. Nao importa nada do
caminho de API (cliente, SDK, lote). `model` reexporta estes nomes (compat com chamadores e monkeypatch de testes).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402
from config import AWAITING, READY  # noqa: E402
from translation_rules import _select_reuse  # noqa: E402


class InvalidTranslationFile(ValueError):
    """translations_<scene_id>.json do subagente ilegivel (nao-UTF-8, JSON quebrado ou sem `lines`)."""


def read_translation(path) -> dict:
    """Le o translations_<scene_id>.json com erro claro. Nao aceita nem converte outra codificacao (cp1252 e
    afins sao so diagnosticados): o subagente regrava o arquivo em UTF-8."""
    path = Path(path)
    fix = "regrave com json.dumps(..., ensure_ascii=False) e open(..., 'w', encoding='utf-8')"
    try:
        data = json.loads(path.read_bytes().decode("utf-8"))
    except UnicodeDecodeError as e:
        raise InvalidTranslationFile(f"{path.name} nao esta em UTF-8 (byte {e.start}); {fix}") from e
    except json.JSONDecodeError as e:
        raise InvalidTranslationFile(f"{path.name} nao e JSON valido (linha {e.lineno}, coluna {e.colno}: "
                                     f"{e.msg}); {fix}") from e
    if not isinstance(data, dict) or not isinstance(data.get("lines"), dict):
        raise InvalidTranslationFile(f"{path.name} sem o objeto `lines` ({{offset: {{...}}}}); {fix}")
    return data


def translate_in_session(root, scene, pack: dict, out: Path):
    """Ramo in-session de `model.translate`: dedup por TM e prompt reduzido; devolve READY ou AWAITING."""
    scene_id = pack["scene_id"]
    # mesmo DEDUP por TM do caminho api: fala ja traduzida em outra cena nao vai ao agente (sai do
    # prompt) e e acrescentada aqui. So preenche offset AUSENTE -- o que o agente escreveu prevalece.
    reuse = _select_reuse(pack, enabled=True)
    data = read_translation(out) if out.is_file() else None      # ilegivel: erro claro, nao api_translate_failed
    if reuse and (data is not None or len(reuse) == pack["n_lines"]):
        data = data if data is not None else {"lines": {}}
        add = {o: e for o, e in reuse.items() if o not in data.setdefault("lines", {})}
        if add:
            data["lines"].update(add)
            paths.atomic_write(out, json.dumps(data, ensure_ascii=False, indent=2))
    elif reuse:
        novel = [r for r in pack["lines"] if r["offset"] not in reuse]   # copia: o pack (e o caminho api) nao muda
        paths.atomic_write(paths.scene_prompt(root, scene), context_pack.render_prompt({**pack, "lines": novel, "n_lines": len(novel)},
                                       context_pack._read(context_pack.CARTA_PATH)))
    if out.is_file():
        return {"status": READY, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"]}
    return {"status": AWAITING, "scene_id": scene_id, "n_lines": pack["n_lines"],
            "prompt": str(paths.scene_prompt(root, scene)),
            "expected_output": str(out)}
