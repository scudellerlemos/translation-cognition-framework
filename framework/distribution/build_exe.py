"""Gera o .exe de um clique. Uso: build_exe.py <dist_do_pacote> <saida_dir> (nome do exe vem do manifest.json)."""
import json
import pathlib
import subprocess
import sys

dist, saida = (pathlib.Path(a).resolve() for a in sys.argv[1:3])
nome = json.loads((dist / 'manifest.json').read_text(encoding='utf-8'))['app']['exe']
ico = [f'--icon={dist / "icone.ico"}'] if (dist / 'icone.ico').is_file() else []
subprocess.run([sys.executable, '-m', 'PyInstaller', '--onefile', '--windowed', *ico, '--name', nome, '--add-data', f'{dist};.',
                '--distpath', str(saida), '--workpath', str(saida / 'work'), '--specpath', str(saida / 'work'),
                str(pathlib.Path(__file__).parent / 'patcher.py')], check=True, capture_output=True)
print(saida / (nome + '.exe'))
