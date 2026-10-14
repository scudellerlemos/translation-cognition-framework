"""Texto repetido entre cenas e traduzido UMA vez (caminho de sessao e de API).

Cenas com a mesma sequencia de `text_source` formam um grupo: traduz-se so a primeira (representante);
`copy` leva traducao e retrotraducao verificadas para as outras, remapeando os offsets por POSICAO no
dialogs.csv (o indice de secao pode diferir). A copia nao pula gate: devolve a lista para o run_scene
passar cada uma pelos gates.

  python scene_dedup.py <projeto> plan     lista os grupos (representante <- copias) e as falas poupadas
  python scene_dedup.py <projeto> copy     copia do representante verified para as copias ainda nao verified
"""
import contextlib
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import context_pack  # noqa: E402
import paths  # noqa: E402


def _rows(root, scene):
    with paths.dialogs(root, scene).open(encoding="utf-8-sig", newline="") as fh:
        return [(r["offset"], r.get("text_source", "")) for r in csv.DictReader(fh)]


def _verified(root, scene) -> bool:
    p = paths.run_state(root)
    st = json.loads(p.read_text(encoding="utf-8")).get("scenes", {}) if p.is_file() else {}
    return st.get(scene, {}).get("status") == "verified"


def groups(root) -> dict[str, list[str]]:
    """{representante: [copias]} so de grupos com 2+ cenas; representante = a primeira em ordem de nome."""
    by: dict[tuple, list[str]] = {}
    for d in sorted(paths.scenes_dir(root).iterdir()):
        if paths.dialogs(root, d.name).is_file():
            by.setdefault(tuple(t for _, t in _rows(root, d.name)), []).append(d.name)
    return {g[0]: g[1:] for k, g in by.items() if len(g) > 1 and k}


def copy(root) -> list[str]:
    """Copia traducao/retrotraducao do representante verified para cada copia nao verified. Regrava sempre
    (o representante pode ter sido corrigido depois). Devolve as cenas tocadas."""
    todo = []
    for rep, dups in groups(root).items():
        if not _verified(root, rep):
            continue
        rid = context_pack.scene_id_of(rep)
        for d in dups:
            if _verified(root, d):
                continue
            m = dict(zip((o for o, _ in _rows(root, rep)), (o for o, _ in _rows(root, d)), strict=True))
            did = context_pack.scene_id_of(d)
            for fn in (paths.translations, paths.back_translation):
                src = fn(root, rep, rid)
                if src.is_file():
                    txt = re.sub(r'"([^"\\]+)"', lambda g, m=m: json.dumps(m.get(g.group(1), g.group(1))),
                                 src.read_text(encoding="utf-8"))
                    fn(root, d, did).write_text(txt, encoding="utf-8")
            todo.append(d)
    return todo


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    if len(sys.argv) != 3 or sys.argv[2] not in ("plan", "copy"):
        sys.exit(__doc__)
    root = paths.require_project(sys.argv[1])
    g = groups(root)
    if sys.argv[2] == "plan":
        saved = sum(len(_rows(root, r)) * len(d) for r, d in g.items())
        for r, d in g.items():
            print(f"{r} <- {', '.join(d)}")
        print(f"{len(g)} grupo(s); {saved} fala(s) a menos para traduzir")
    else:
        print(" ".join(copy(root)))


if __name__ == "__main__":
    main()
