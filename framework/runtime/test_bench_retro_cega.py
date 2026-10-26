"""test_bench_retro_cega.py — sorteio, montagem dos dois bracos e placar do benchmark da retrotraducao cega."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import bench_retro_cega as b  # noqa: E402
import paths  # noqa: E402


def _projeto(root: Path, n: int = 6):
    sd = root / "artifacts" / "scenes" / "S1"
    sd.mkdir(parents=True)
    (root / "project.json").write_text('{"title":"T"}', encoding="utf-8")
    linhas = ["offset,scene,file,idx,text_en,byte_budget"]
    tr = {}
    for i in range(n):
        linhas.append(f"{i},S1,f,{i},This is a long enough line number {i},99")
        tr[str(i)] = {"t": f"Esta e a fala numero {i}", "speaker": "Ryu"}
    (sd / "dialogs.csv").write_text("\n".join(linhas), encoding="utf-8")
    paths.translations(root, "S1", "S1").write_text(json.dumps({"lines": tr}), encoding="utf-8")


def test_sorteio_e_determinista_e_marca_metade_com_defeito(tmp_path):
    _projeto(tmp_path)
    a, c = b.sorteio(tmp_path, n=6, seed=3, por_cena=6), b.sorteio(tmp_path, n=6, seed=3, por_cena=6)
    assert a == c and len(a) == 6 and sum(x["defeito"] for x in a) == 3
    assert len({x["id"] for x in a}) == 6


def test_montar_gera_prompts_nos_dois_bracos_e_so_a_cega_separa_o_source(tmp_path):
    _projeto(tmp_path / "p")
    casos = b.sorteio(tmp_path / "p", n=4, seed=1, por_cena=4)
    defeitos = {x["id"]: {"target": "alterada " + x["id"], "tipo": "tom"} for x in casos if x["defeito"]}
    b.montar(tmp_path / "w", casos, defeitos)
    sd = "artifacts/scenes/S1"
    assert (tmp_path / "w" / "padrao" / sd / "back_prompt_S1.md").is_file()
    assert not (tmp_path / "w" / "padrao" / sd / "back_prompt_juiz_S1.md").exists()
    a = (tmp_path / "w" / "cega" / sd / "back_prompt_S1.md").read_text(encoding="utf-8")
    assert "long enough line" not in a
    assert "long enough line" in (tmp_path / "w" / "cega" / sd / "back_prompt_juiz_S1.md").read_text(encoding="utf-8")


def _grava(proj: Path, vered: dict):
    sd = proj / "artifacts" / "scenes" / "S1"
    sd.mkdir(parents=True, exist_ok=True)
    ents = [{"offset": f"S1:{k}", "verdict": v} for k, v in vered.items()]
    (sd / "back_translation_S1.json").write_text(json.dumps({"entries": ents}), encoding="utf-8")


def test_placar_calcula_recall_falso_alarme_e_criterio(tmp_path):
    casos = [{"id": f"C{i}", "defeito": i < 2} for i in range(4)]
    defeitos = {"C0": {"tipo": "tom"}, "C1": {"tipo": "omissao"}}
    (tmp_path / "casos.json").write_text(json.dumps(casos), encoding="utf-8")
    (tmp_path / "defeitos.json").write_text(json.dumps(defeitos), encoding="utf-8")
    _grava(tmp_path / "padrao", {"C0": "revise", "C1": "pass", "C2": "pass", "C3": "pass"})
    _grava(tmp_path / "cega", {"C0": "revise", "C1": "revise", "C2": "pass", "C3": "pass"})
    r = b.placar(tmp_path)
    assert r["padrao"]["recall"] == 0.5 and r["cega"]["recall"] == 1.0
    assert r["cega"]["falso_alarme"] == 0.0 and r["adotar_cega"] is True
    assert r["cega"]["por_tipo"] == {"omissao": "1/1", "tom": "1/1"}


def test_placar_nao_adota_com_veredito_faltando(tmp_path):
    casos = [{"id": "C0", "defeito": True}, {"id": "C1", "defeito": False}]
    (tmp_path / "casos.json").write_text(json.dumps(casos), encoding="utf-8")
    (tmp_path / "defeitos.json").write_text(json.dumps({"C0": {"tipo": "tom"}}), encoding="utf-8")
    _grava(tmp_path / "padrao", {"C0": "pass", "C1": "pass"})
    _grava(tmp_path / "cega", {"C0": "revise"})
    r = b.placar(tmp_path)
    assert r["cega"]["sem_veredito"] == 1 and r["adotar_cega"] is False
