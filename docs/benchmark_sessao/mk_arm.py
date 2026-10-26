"""Cria um braco isolado do benchmark em output/bench_<nome>/ a partir do snapshot B2."""
import json
import pathlib
import shutil
import sys

nome = sys.argv[1]
P = pathlib.Path('projects/utawarerumono_prelude')
snap = P / 'output/bench_b2_inicial'
dst = P / f'output/bench_{nome}'
if dst.exists(): sys.exit(f'{dst} ja existe')
dst.mkdir(parents=True)
for d in ('connector', 'backup_original'):
    shutil.copytree(P / d, dst / d)
shutil.copytree(snap / 'profile', dst / 'profile')
shutil.copytree(snap / 'artifacts', dst / 'artifacts')
shutil.copy(snap / 'utawarerumono_prelude.db', dst / 'utawarerumono_prelude.db')
for f in ('dialogs.csv', 'ordem_cenas.txt'):
    shutil.copy(P / 'artifacts' / f, dst / 'artifacts' / f)
for c in (sys.argv[2:] or ('00_00_04', '00_01_01', '00_03_01', '00_03_02', '00_04_04', '00_90_01')):
    (dst / 'artifacts/scenes' / c).mkdir(parents=True)
    shutil.copy(P / 'artifacts/scenes' / c / 'dialogs.csv', dst / 'artifacts/scenes' / c / 'dialogs.csv')
cfg = json.load(open(P / 'project.json', encoding='utf-8'))
cfg['series'] = f'bench_{nome}'
cfg['hitl_fila'] = 'diferida'
json.dump(cfg, open(dst / 'project.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
shutil.copy(P / 'artifacts/research_log.md', dst / 'artifacts/research_log.md')
rs = json.load(open(P / 'artifacts/run_state.json', encoding='utf-8'))
json.dump({'scenes': {}, 'managed_by': rs.get('managed_by')}, open(dst / 'artifacts/run_state.json', 'w'), indent=1)
bp = dst / 'connector/build_plan_chapter.py'
bp.write_text(bp.read_text(encoding='utf-8').replace('ROOT.parent.parent / "framework"', 'ROOT.parents[3] / "framework"'), encoding='utf-8')
ex = dst / 'connector/extract.py'
ex.write_text(ex.read_text(encoding='utf-8').replace('.parents[3] / "framework"', '.parents[5] / "framework"'), encoding='utf-8')
print('ok', dst)
