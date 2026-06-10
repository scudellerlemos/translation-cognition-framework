#!/usr/bin/env python3
"""
naturalness_lint.py — Linter de naturalidade (governança de tradução), irmão heurístico do
`validate.py`. Sinaliza "smells" de tradução que a amostragem humana costuma deixar passar — saída
são CANDIDATOS para revisão (06c), não auto-fix.

Genérico e sem dados de obra: lê `project.json` + artefatos (`translation_plan.json` ou
`dialogs.csv`+`approved_translations.csv`) e o `glossary.csv` (whitelist). Checagens de alta precisão:

- `copia_crua`        : alvo idêntico ao source (normalizado), fora da whitelist (termos de glossário
                        `manter_original`; onomatopeia pura de vogais como `Aaaah!`). Pega interjeição/
                        linha não traduzida.
- `fragmento_residual`: linha onde alvo e source diferem, mas compartilham um CHUNK INICIAL curto e
                        idêntico (≤2 letras) — pega o `U...` em `U... Argh...`.
- `rotulo_cru`        : rótulo de falante (alias/UI) ainda idêntico ao source.

Uso:  python naturalness_lint.py <dir-do-projeto>     (default: diretório atual)
Saída: imprime os achados + grava `<projeto>/artifacts/naturalness_lint.json`.
"""
from __future__ import annotations
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

VOWELS_H = set("aeiouh")              # onomatopeia "pura" (gritos/suspiros) — cópia aceitável


def _norm(s: str) -> str:
    s = (s or "").replace("\\n", " ")
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).strip().lower()


def _alpha(s: str) -> str:
    return "".join(c for c in s.lower() if c.isalpha())


def _is_pure_onomatopoeia(s: str) -> bool:
    a = _alpha(_norm(s))
    if not a:
        return False
    if set(a) <= VOWELS_H:                           # só vogais/h: "Aaaah!", "Ah...!"
        return True
    return bool(re.search(r"([aeiou])\1\1", a))       # vogal repetida 3+ = grito: "Aaagh--", "Eeee!"


def _csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def lint_project(root: Path) -> list[dict]:
    """Retorna lista de achados: {offset, check, speaker, source, target, note}."""
    root = Path(root)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    idc = (cfg.get("source", {}) or {}).get("id_column", "offset")
    tokens = cfg.get("formatting_tokens", []) or []
    # tokens parametrizados (cor {c<N>}/{c-1}/{c-}, etc.): regex, não literais
    rx_tokens = [re.compile(p) for p in (cfg.get("formatting_token_patterns", []) or [])]
    art = root / "artifacts"

    def strip_tokens(s: str) -> str:
        for tk in tokens:
            s = s.replace(tk, " ")
        for rx in rx_tokens:
            s = rx.sub(" ", s)
        return s

    # pares (offset, source, target, speaker) — do plano se houver; senão dialogs + approved
    pairs = []
    plan_f = art / "translation_plan.json"
    if plan_f.is_file():
        for l in json.loads(plan_f.read_text(encoding="utf-8")).get("lines", []):
            pairs.append((l.get("offset"), l.get("text_source", ""),
                          l.get("base_translation", ""), l.get("speaker", "")))
    else:
        src = {}
        if (art / "dialogs.csv").is_file():
            for r in _csv(art / "dialogs.csv"):
                src[r.get(idc)] = r.get("text_source", "")
        if (art / "approved_translations.csv").is_file():
            for r in _csv(art / "approved_translations.csv"):
                pairs.append((r.get(idc), src.get(r.get(idc), ""), r.get("text_target", ""), ""))

    # whitelist: termos de glossário manter_original (por conteúdo alfabético) + aliases/UI (p/ rótulo)
    keep_alpha = set()
    labels = set()
    if (art / "glossary.csv").is_file():
        for r in _csv(art / "glossary.csv"):
            if (r.get("handling_rule") or "").strip() == "manter_original":
                keep_alpha.add(_alpha(r.get("term", "")))
            if (r.get("category") or "") == "UI":
                labels.add(_norm(r.get("term", "")))
    am = art / "aliases_map.json"
    if am.is_file():
        for a in json.loads(am.read_text(encoding="utf-8")).get("aliases", []):
            labels.add(_norm(a.get("alias", "")))

    found = []
    def add(off, chk, spk, s, t, note):
        found.append({"offset": off, "check": chk, "speaker": spk,
                      "source": s, "target": t, "note": note})

    for off, s, t, spk in pairs:
        ns, nt = _norm(s), _norm(t)
        if not ns or not nt:
            continue
        if ns == nt:                                  # idêntico ao source
            a = _alpha(strip_tokens(s))               # conteúdo alfabético sem tokens
            if not a or a in keep_alpha or _is_pure_onomatopoeia(strip_tokens(s)):
                continue                              # numérico/símbolos / nome próprio / grito puro: ok
            if ns in labels:
                add(off, "rotulo_cru", spk, s, t, "rótulo de falante idêntico ao source — localizar")
            else:
                add(off, "copia_crua", spk, s, t, "alvo idêntico ao source — traduzir/localizar")
            continue
        # fragmento inicial residual: stub de 1 letra + reticências idêntico (ex.: "U..."),
        # com o resto traduzido. "X..." é hesitação; "a short" (1 letra + espaço) é palavra real → ignora.
        ms = re.match(r"^([^\W\d_])\.\.\.", (s or "").strip())
        mt = re.match(r"^([^\W\d_])\.\.\.", (t or "").strip())
        if ms and mt and ms.group(1).lower() == mt.group(1).lower():
            add(off, "fragmento_residual", spk, s, t,
                f"hesitação inicial '{ms.group(1)}...' copiada do source — localizar")

    return found


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    found = lint_project(root)
    out = root / "artifacts" / "naturalness_lint.json"
    out.write_text(json.dumps({"count": len(found), "findings": found},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    by = {}
    for f in found:
        by[f["check"]] = by.get(f["check"], 0) + 1
        print(f"{f['check']:18} {f['offset']:>9}  {f['source']!r} -> {f['target']!r}")
    print(f"\n{len(found)} candidato(s) " + (f"({by})" if by else "") + f" -> {out}")
    sys.exit(0)


if __name__ == "__main__":
    main()
