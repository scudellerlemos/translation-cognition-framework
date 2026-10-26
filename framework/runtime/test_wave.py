import argparse
import subprocess
import wave

import paths


def _proj(root):
    (root / "project.json").write_text("{}", encoding="utf-8")
    for sc in ("ch_1_01", "ch_1_02", "ch_1_03"):
        d = paths.scene_dir(root, sc)
        d.mkdir(parents=True)
        txt = "Bye" if sc == "ch_1_03" else "Hi"
        (d / "dialogs.csv").write_text(f"offset,text_source\nX:{sc}:1,{txt}\n", encoding="utf-8")
    (root / "artifacts").mkdir(exist_ok=True)


def test_duplicate_scene_waits_for_original_then_goes_through_gates(tmp_path, monkeypatch):
    _proj(tmp_path)
    names = [n for n, _ in wave.steps(str(tmp_path), ["ch_1_01", "ch_1_02", "ch_1_03"], "in-session", False)]
    assert names[:2] == ["run_scene", "scene_dedup"]
    ran = []

    def fake(cmd, **k):
        ran.append(cmd[3:])
        out = "ch_1_02" if cmd[3].endswith("scene_dedup.py") else "ok"
        return argparse.Namespace(returncode=0, stdout=out, stderr="")
    monkeypatch.setattr(subprocess, "run", fake)
    assert wave.run(str(tmp_path), ["ch_1_01", "ch_1_02", "ch_1_03"]) == 0
    runs = [c for c in ran if c[0].endswith("run_scene.py")]
    assert len(runs) == 2 and "ch_1_02" not in runs[0] and "ch_1_02" in runs[1]


def test_no_duplicates_keeps_old_steps(tmp_path):
    _proj(tmp_path)
    assert "scene_dedup" not in [n for n, _ in wave.steps(str(tmp_path), ["ch_1_03"], "api", False)]


def test_dedup_copy_is_limited_to_requested_scenes(tmp_path):
    import scene_dedup
    _proj(tmp_path)
    d = paths.scene_dir(tmp_path, "ch_1_04")
    d.mkdir()
    (d / "dialogs.csv").write_text("offset,text_source\nX:ch_1_04:1,Hi\n", encoding="utf-8")
    rs = paths.run_state(tmp_path)
    rs.write_text('{"scenes": {"ch_1_01": {"status": "verified"}}}', encoding="utf-8")
    assert scene_dedup.copy(tmp_path, only=["ch_1_02"]) == ["ch_1_02"]


def test_wave_rebuilds_session_cost_before_reporting(tmp_path):
    _proj(tmp_path)
    names = [n for n, _ in wave.steps(str(tmp_path), [], "in-session", False)]
    assert names.index("session_usage") < names.index("cost_report") < names.index("cost_detail")


def test_summary_line_shows_session_equivalent_not_just_zero():
    import cost_report
    rep = {"total_usd": 0.0, "verified_scenes": 7, "n_calls": 30, "by_stage": {"3": {"usd": 2.65, "calls": 155}},
           "by_source": {"session": {"api_equiv_usd": 4.35, "calls": 252}}, "out_est": 44, "tokens": {"out": 100}}
    line = cost_report.summary_line(rep)
    assert "$4.35" in line and "3 $2.65" in line and "44%" in line
    assert "$4.35" not in cost_report.summary_line({**rep, "by_source": {}})


def test_wave_echoes_phase_lines_that_session_usage_reads(tmp_path, monkeypatch, capsys):
    """sem AGUARDANDO/`status final` na saida o session_usage nao separa traducao de governanca nem fecha a cena."""
    import session_usage
    _proj(tmp_path)
    out = chr(10).join(["Loading weights", "[2/6] AGUARDANDO traducao (caminho assinatura): responda",
                   "      AGUARDANDO back-translation: p.md", "OK run_scene ch_1_01: status final = verified", "ruido"])
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: argparse.Namespace(returncode=0, stdout=out, stderr=""))
    wave.run(str(tmp_path), ["ch_1_01"])
    shown = capsys.readouterr().out
    assert "AGUARDANDO traducao" in shown and "AGUARDANDO back-translation" in shown and "Loading weights" not in shown
    assert session_usage._CLOSE.findall(shown) == ["ch_1_01"]
    assert wave.phase_lines("glossary_lint", out) == []


def test_single_scene_gets_its_own_log_so_parallel_agents_do_not_overwrite():
    assert wave.log_name(["00_01_01"]) == "wave_last_00_01_01.log"
    assert wave.log_name([]) == "wave_last.log"
    assert wave.log_name(["a", "b", "c"]) == "wave_last_a_+2.log"           # onda de varias cenas tambem nao sobrescreve a anterior


def test_glossary_lint_step_is_scoped_to_the_requested_scenes(tmp_path):
    _proj(tmp_path)
    p = str(tmp_path)
    scoped = dict(wave.steps(p, ["ch_1_03"], "api", False))["glossary_lint"]
    assert scoped == ["glossary_lint.py", p, "--scenes", "ch_1_03"]         # onda: so cena do pedido bloqueia
    assert dict(wave.steps(p, [], "api", False))["glossary_lint"] == ["glossary_lint.py", p]


def test_new_wave_is_blocked_by_escalation_left_open_in_another_scene(tmp_path):
    import hitl
    (tmp_path / "project.json").write_text('{"hitl": true}', encoding="utf-8")
    for sc in ("A", "B"):
        paths.scene_dir(tmp_path, sc).mkdir(parents=True)
    item = {"scene": "A", "offset": "A:1", "term": "", "kind": "tradutor", "alias": "", "correcao": ""}
    hitl.enqueue(tmp_path, [item])
    p = str(tmp_path)
    assert "A" in wave.entry_problems(p, ["B"])[0]                          # onda nova (B sem pack): bloqueia
    assert wave.run(p, ["B"]) == 1                                          # e o `wave` nem comeca
    paths.pack(tmp_path, "B").write_text("{}", encoding="utf-8")
    assert wave.entry_problems(p, ["B"]) == []                              # B ja em andamento: irma em paralelo nao trava
    assert wave.entry_problems(p, []) == []


def test_step_that_hangs_stops_the_wave_with_timeout_message(tmp_path, monkeypatch, capsys):
    _proj(tmp_path)

    def trava(cmd, **k):
        assert k["timeout"] == 5
        raise subprocess.TimeoutExpired(cmd, k["timeout"])
    monkeypatch.setattr(subprocess, "run", trava)
    assert wave.run(str(tmp_path), ["ch_1_03"], step_timeout=5) == 124
    assert "sem resposta em 5 s" in capsys.readouterr().out
    assert "TIMEOUT apos 5 s" in (tmp_path / "artifacts" / "wave_last_ch_1_03.log").read_text(encoding="utf-8")


def test_espera_esperada_nao_alerta_so_com_marca_de_espera_e_sem_erro():
    assert wave.espera_esperada("run_scene", "[3/6] AGUARDANDO back-translation: x\nLOTE: 0/1")
    assert wave.espera_esperada("run_scene_copias", "AGUARDANDO traducao (caminho assinatura)")
    assert wave.espera_esperada("quality_gate", "SEM COBERTURA - 3 linha(s) high/critical")
    assert not wave.espera_esperada("run_scene", "AGUARDANDO traducao\nTraceback (most recent call last)")
    assert not wave.espera_esperada("quality_gate", "SEM COBERTURA\nERRO: schema")
    assert not wave.espera_esperada("glossary_lint", "SEM COBERTURA")
    assert not wave.espera_esperada("run_scene", "falhou por outro motivo")
    # defeito da traducao (token/schema/glifo): a sessao corrige e roda de novo; so Traceback segue sendo falha
    corrige = f"{wave.events.CORRECAO_MARCA} (build_plan): ajuste\nSCHEMA: 1 erro(s)"
    assert wave.espera_esperada("run_scene", corrige) and wave.espera_esperada("run_scene_copias", corrige)
    assert not wave.espera_esperada("run_scene", corrige + "\nTraceback (most recent call last)")
    assert not wave.espera_esperada("quality_gate", corrige)
