"""session_usage.py — tokens REAIS gastos nas sessoes do Claude Code (backend in-session).

No backend in-session quem traduz e a propria sessao; nao ha chamada de API do harness. O Claude Code
grava o `usage` exato de cada requisicao em `~/.claude/projects/<projeto>/<sessao>.jsonl` e, para cada
subagente, em `<sessao>/subagents/agent-<id>.jsonl`. `sync` le essas transcricoes e anexa ao
api_ledger.jsonl linhas `source: "session"` (linha sem `source` = chamada de API do harness, cobrada).

Como cada requisicao e atribuida (`attribution`):
  agent    — subagente que rodou `run_scene` de UMA cena: tudo o que ele gastou e da cena. EXATO.
  window   — sessao principal (ou subagente de varias cenas): enquanto o ultimo `run_scene` da cena
             respondeu AGUARDANDO (traducao ou back-translation). Aproximado: cenas em lote dividem pela
             mais recente, e conversa no meio da janela entra junto.
  overhead — o resto da sessao PRINCIPAL (orquestracao, conversa): cena `_session`.
  Requisicao de SUBAGENTE sem cena (o de varias cenas: retraducao do passo 5d, retrotraducao) nao e overhead: e `agent`
  na cena `_session`, com `agent_type` (do .meta.json do subagente) para separar tradução de verificação.
Cada linha traz tambem `phase`, pelo que o ultimo `run_scene` respondeu: `translate` (AGUARDANDO traducao),
`back` (AGUARDANDO back-translation = governanca) ou `other` (empacotar, verificar, conversa).
O TOTAL por sessao e sempre exato (cada requisicao entra uma vez, por id). So entram sessoes que rodaram
`run_scene` em alguma cena deste projeto. Incremental e idempotente: um cursor por arquivo de transcricao
(`until`) — rodar de novo so anexa o que e novo, inclusive de sessoes antigas ainda em disco.

`cost_usd` e 0.0 (assinatura, nao sai do saldo da API); `api_equiv_usd` e o que custaria na API.

`stage` e a fase do projeto, por MARCA EXPLICITA: `python session_usage.py mark <projeto> <fase>` grava a
virada em `artifacts/phase_marks.jsonl` e toda requisicao a partir dali (janela e subagentes) cai nessa fase.

Saida: a transcricao de subagente nem sempre grava o `usage` final da mensagem (fica o parcial do stream, 2 a
20 tokens). Nessas a saida e ESTIMADA pelo tamanho do conteudo gravado (`_OUT_FIT`) e a linha traz `out_est` =
quantos tokens de `usage.out` sao estimativa. Mensagem com `stop_reason` gravado e sempre o numero exato.

As linhas `overhead` trazem `activity`: o que a requisicao estava fazendo, pelo comando ou arquivo que ela
tocou (`_ACTIVITY`, primeira regra que casa; sem ferramenta = `conversa`). E HEURISTICA — o total segue exato.

GOVERNANCA: da transcricao sai so contador de token, nome de modelo, id de cena e o status final do
`run_scene`; nenhum texto e copiado.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import cost
import paths  # noqa: E402

OVERHEAD = "_session"
_CLOSE = re.compile(r"run_scene (\S+): status final = verified")
# comando que roda uma cena: o run_scene direto ou o wave.py (que o chama por dentro; sem ele a sessao some do ledger)
_RUNNER = re.compile(r"(?<![\w])(?:run_scene|wave)\.py")
# ponytail: classificacao por palavra-chave no comando/caminho; trocar por marcacao explicita se as
# categorias passarem a decidir orcamento.
_ACTIVITY = [(a, re.compile(rx, re.I)) for a, rx in [
    ("jogo", r"steamapps|teste_ingame"),
    ("conector", r"connector[/\\]|source_dat|\.dat\b|binwalk|kaitai"),
    ("kb", r"glossary|entities|kb_|research_|worklist"),
    ("pipeline", r"run_scene|run_chapter|artifacts[/\\]+scenes|translations_|back_translation"),
    ("framework", r"framework[/\\]|pytest|ruff|\.claude[/\\]+hooks|docs[/\\]"),
    ("git", r"\bgit |\bgh "),
]]


# tokens de saida por caractere de (conteudo visivel, assinatura do raciocinio), ajustado nas mensagens que
# TEM o usage final (2026-10-12; erro agregado de 1% a 16% por modelo).
# ponytail: constantes medidas, nao recalculadas; refazer o ajuste se o formato da transcricao mudar.
# Ajuste medido em mensagens com saida exata (7.000+ mensagens do projeto): vies na SOMA entre -7% e +5% por modelo;
# por mensagem o erro e de 8% a 18%. Reajustar com tools de calibracao se um modelo novo aparecer.
_OUT_FIT = {"claude-opus-5-5": (0.34, 0.32), "claude-sonnet-5-5": (0.52, 0.36), "claude-haiku-5-5": (0.72, 0.30),
            "claude-sonnet-5": (0.39, 0.27)}
_OUT_FIT_DEFAULT = (0.44, 0.28)


def _size(blocks: list) -> tuple[int, int]:
    """(caracteres visiveis, caracteres de raciocinio/assinatura) dos blocos de UMA linha da transcricao."""
    vis = sig = 0
    for b in blocks:
        if b.get("type") == "text":
            vis += len(b.get("text") or "")
        elif b.get("type") == "tool_use":
            vis += len(json.dumps(b.get("input"), ensure_ascii=False))
        elif b.get("type") == "thinking":
            sig += len(b.get("signature") or "") + len(b.get("thinking") or "")
    return vis, sig


def marks(root) -> list[tuple[float, str]]:
    p = paths.artifacts(root) / "phase_marks.jsonl"
    rows = paths.read_jsonl(p)
    return sorted((r["t"], r["stage"]) for r in rows)


def mark(root, stage: str, t: float | None = None) -> None:
    """Marca a virada de fase: as requisicoes a partir de agora entram em `stage`."""
    import time
    paths.append_line(paths.artifacts(root) / "phase_marks.jsonl",
                      json.dumps({"t": round(t or time.time(), 3), "stage": stage}, ensure_ascii=False) + "\n")


def _activity(blocks: list) -> str | None:
    uses = [json.dumps(b.get("input"), ensure_ascii=False) for b in blocks if b.get("type") == "tool_use"]
    return next((a for a, rx in _ACTIVITY if any(rx.search(u) for u in uses)), "outros") if uses else None


def _usage(u: dict) -> dict:
    total = max(0, int(u.get("cache_creation_input_tokens") or 0))
    h1 = min(total, max(0, int((u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens") or 0)))  # nunca > total
    return {"in": int(u.get("input_tokens") or 0), "out": int(u.get("output_tokens") or 0),
            "cache_read": int(u.get("cache_read_input_tokens") or 0),
            "cache_write": total - h1,                                            # TTL 5 min (1.25x)
            "cache_write_1h": h1}                                                 # TTL 1 h (2x)


def transcripts_dir(session_id: str | None = None, home: Path | None = None) -> Path | None:
    """Pasta de transcricoes do projeto da sessao corrente (None fora do Claude Code)."""
    sid = session_id or os.environ.get("CLAUDE_CODE_SESSION_ID")
    hits = list(((home or Path.home()) / ".claude" / "projects").glob(f"*/{sid}.jsonl")) if sid else []
    return hits[0].parent if hits else None


def _scan(path: Path, scene_re: re.Pattern) -> tuple[dict, set]:
    """-> ({message.id: [ts, modelo, usage, cena|None, fase, atividade, saida estimada]}, cenas tocadas). 1 requisicao = 1 message.id (a
    transcricao repete a mensagem por bloco de conteudo, vale o 1o timestamp e o ULTIMO usage)."""
    reqs: dict[str, list] = {}
    opened: list[str] = []          # cenas abertas, a mais recente por ultimo
    touched: set[str] = set()
    pending: dict[str, list] = {}   # tool_use.id do comando run_scene -> cenas que ele abriu
    phase = "other"                 # o que o ultimo run_scene ficou esperando
    sizes: dict[str, list] = {}     # message.id -> [chars visiveis, chars de raciocinio, tem usage final?]
    with path.open(encoding="utf-8") as f:
        for line in f:
            rs = "run_scene" in line or "wave.py" in line
            res = next((i for i in pending if i in line), None) if pending else None
            if not rs and not res and '"usage"' not in line:
                continue
            try:
                d = json.loads(line)
                msg = d.get("message") if isinstance(d.get("message"), dict) else {}
                if rs and d.get("type") == "assistant":     # comando que roda o run_scene: abre a(s) cena(s)
                    for b in msg.get("content") or []:
                        cmd = str((b.get("input") or {}).get("command", "")) if b.get("type") == "tool_use" else ""
                        for s in scene_re.findall(cmd) if _RUNNER.search(cmd) else []:
                            touched.add(s)
                            opened = [x for x in opened if x != s] + [s]
                            pending.setdefault(b.get("id", ""), []).append(s)
                elif res and d.get("type") == "user":       # saida do comando: a cena so fica aberta se AGUARDANDO
                    r = d.get("toolUseResult")
                    stdout = str(r.get("stdout", "")) if isinstance(r, dict) else str(r)
                    done = pending.pop(res) if "AGUARDANDO" not in stdout else _CLOSE.findall(stdout)
                    opened = [x for x in opened if x not in done]
                    phase = ("back" if "AGUARDANDO back-translation" in stdout
                             else "translate" if "AGUARDANDO traducao" in stdout else "other")
                u = msg.get("usage")
                if u and msg.get("id"):
                    ts = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).timestamp()
                    q = reqs.setdefault(msg["id"], [ts, msg.get("model", ""), _usage(u), None, phase, None, 0])
                    q[2] = _usage(u)        # vale o ULTIMO usage: o 1o registro traz a saida parcial do stream
                    s = sizes.setdefault(msg["id"], [0, 0, False])
                    vis, sig = _size(msg.get("content") or [])      # cada linha traz um bloco da mensagem
                    s[0], s[1], s[2] = s[0] + vis, s[1] + sig, s[2] or bool(msg.get("stop_reason"))
                    q[3] = opened[-1] if opened else None
                    q[5] = q[5] or _activity(msg.get("content") or [])     # a mensagem se repete por bloco
            except (ValueError, KeyError, AttributeError, TypeError):
                continue
    for mid, (vis, sig, final) in sizes.items():        # sem usage final: estima a saida pelo conteudo
        q = reqs[mid]
        a, b = _OUT_FIT.get(q[1], _OUT_FIT_DEFAULT)
        est = round(a * vis + b * sig)
        if not final and est > q[2]["out"]:
            q[2]["out"], q[6] = est, est
    return reqs, touched


_SCAN_MEMO: dict = {}


def _scan_cached(path: Path, scene_re: re.Pattern) -> tuple[dict, set]:
    """_scan memoizado por processo: num lote o sync roda a cada cena e relia todas as transcricoes; a
    que nao mudou (mesmo tamanho e mtime) nao e relida. O resultado e so lido pelo chamador."""
    st = path.stat()
    key = (str(path), st.st_mtime_ns, st.st_size, scene_re.pattern)
    if key not in _SCAN_MEMO:
        _SCAN_MEMO[key] = _scan(path, scene_re)
    return _SCAN_MEMO[key]


def _known_scenes(root: Path) -> set[str]:
    p, d = paths.run_state(root), paths.scenes_dir(root)
    names = set(json.loads(p.read_text(encoding="utf-8")).get("scenes", {})) if p.is_file() else set()
    return names | ({x.name for x in d.iterdir() if x.is_dir()} if d.is_dir() else set())


def _session_rows(root: Path) -> list[dict]:
    lp = paths.ledger(root)
    rows = []
    for line in lp.read_text(encoding="utf-8").splitlines() if lp.is_file() else []:
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("source") == "session":
            rows.append(r)
    return rows


def _agent_type(transcript: Path) -> str | None:
    """`agentType` do .meta.json ao lado da transcricao do subagente (None se faltar ou estiver ilegivel)."""
    try:
        return json.loads(transcript.with_suffix(".meta.json").read_text(encoding="utf-8")).get("agentType")
    except (OSError, ValueError):
        return None


def sync(root, tdir: Path | None = None) -> list[dict]:
    """Anexa ao ledger o que as transcricoes tem de novo. Devolve as linhas anexadas."""
    root = Path(root)
    tdir = tdir or transcripts_dir()
    names = _known_scenes(root)
    if tdir is None or not names:
        return []
    scene_re = re.compile(r"(?<![\w.])(" + "|".join(map(re.escape, sorted(names, key=len, reverse=True))) + r")(?![\w.])")
    cursor: dict[tuple, float] = {}
    for r in _session_rows(root):
        k = (r.get("session"), r.get("agent"))
        cursor[k] = max(cursor.get(k, 0.0), r.get("until", 0.0))
    out = []
    stages = marks(root)
    # ponytail: sessao que nunca tocou o projeto e relida a cada sync (so filtro de texto, sem JSON);
    # guardar um indice de arquivos ja descartados se a pasta de transcricoes ficar grande demais.
    for main in sorted(tdir.glob("*.jsonl")):
        files = [(None, main)] + [(a.stem[6:], a) for a in sorted((tdir / main.stem / "subagents").rglob("agent-*.jsonl"))]
        sid = main.stem[:8]
        if all(a.stat().st_mtime <= cursor.get((sid, aid), -1) for aid, a in files):
            continue
        tipos = {aid: _agent_type(a) for aid, a in files if aid}
        scans = [(aid, *_scan_cached(a, scene_re)) for aid, a in files]
        if not any(touched for _, _, touched in scans):
            continue
        for aid, reqs, touched in scans:
            new = [q for q in reqs.values() if q[0] > cursor.get((sid, aid), 0.0)]
            if not new:
                continue
            only = next(iter(touched)) if aid and len(touched) == 1 else None
            agg: dict[tuple, dict] = {}
            for ts, model, u, scene, phase, act, est in new:
                scene, how = (only, "agent") if only else (scene, "window") if scene else (OVERHEAD, "agent" if aid else "overhead")
                phase, act = ("other", act or "conversa") if how == "overhead" else (phase, None)
                stage = next((s for t, s in reversed(stages) if t <= ts), None)
                a = agg.setdefault((scene, model, phase, act, stage), {"t": 0.0, "n": 0, "how": how, "usd": 0.0, "est": 0,
                                                                       "usage": dict.fromkeys(u, 0)})
                a["t"], a["n"], a["est"] = max(a["t"], ts), a["n"] + 1, a["est"] + est
                a["usd"] += cost.cost_of(model, u) if model in cost._PRICE else 0.0     # por requisicao (degrau do Haiku)
                for k, v in u.items():
                    a["usage"][k] += v
            until = round(max(q[0] for q in new), 3)
            for (scene, model, phase, act, stage), a in sorted(agg.items(), key=lambda kv: tuple(map(str, kv[0]))):
                out.append({"t": round(a["t"], 3), "scene": scene, "kind": "session", "source": "session", "phase": phase,
                            **({"activity": act} if act else {}), **({"stage": stage} if stage else {}),
                            **({"out_est": a["est"]} if a["est"] else {}),
                            **({"agent_type": tipos[aid]} if aid and tipos.get(aid) else {}),
                            "session": sid, "agent": aid, "attribution": a["how"], "model": model, "batch": False,
                            "usage": a["usage"], "n_requests": a["n"], "until": until, "cost_usd": 0.0,
                            "api_equiv_usd": round(a["usd"], 5) if model in cost._PRICE else None})
    if out:
        cost._ledger_append(paths.ledger(root), "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    return out


def rebuild(root) -> list[dict]:
    """Refaz as linhas de sessao a partir das transcricoes inteiras (1 requisicao = 1 message.id). Use ao fechar
    uma medicao: o sync incremental pode pegar mensagem ainda em andamento. As linhas de API ficam intactas."""
    lp = paths.ledger(root)
    with paths.locked(lp):          # appenders do ledger usam a mesma trava: nenhuma linha de API se perde
        keep = [x for x in lp.read_text(encoding="utf-8").splitlines() if json.loads(x).get("source") != "session"]
        paths.atomic_write(lp, "".join(x + "\n" for x in keep))
    return sync(root)


def scene_total(root, scene: str) -> dict | None:
    """Soma das linhas de sessao de uma cena no ledger (None se nao ha nenhuma)."""
    rows = [r for r in _session_rows(Path(root)) if r.get("scene") == scene]
    if not rows:
        return None
    usage: dict[str, int] = {}
    for r in rows:
        for k, v in r["usage"].items():
            usage[k] = usage.get(k, 0) + v
    eq = [r.get("api_equiv_usd") for r in rows]
    return {"usage": usage, "n_requests": sum(r["n_requests"] for r in rows),
            "models": sorted({r["model"] for r in rows}), "attribution": sorted({r["attribution"] for r in rows}),
            "api_equiv_usd": None if None in eq else round(sum(x for x in eq if x is not None), 5)}


if __name__ == "__main__":      # python session_usage.py <projeto> [pasta] | mark <projeto> <fase> | rebuild <projeto>
    if sys.argv[1] == "rebuild":
        raise SystemExit(print(f"session_usage: ledger refeito, {len(rebuild(sys.argv[2]))} linha(s) de sessao."))
    if sys.argv[1] == "mark":
        if not re.fullmatch(r"\d+", sys.argv[3]):      # rotulo = numero da fase; "translate" etc. viram fase solta no ledger
            raise SystemExit(f"ERRO: fase '{sys.argv[3]}' invalida: use o numero da fase (ex.: 3).")
        sync(sys.argv[2])           # fecha a fase anterior antes de marcar a nova
        mark(sys.argv[2], sys.argv[3])
        raise SystemExit(print(f"session_usage: fase '{sys.argv[3]}' marcada."))
    new = sync(sys.argv[1], Path(sys.argv[2]) if len(sys.argv) > 2 else None)
    print(f"session_usage: {len(new)} linha(s) nova(s), {sum(r['n_requests'] for r in new)} requisicao(oes).")
