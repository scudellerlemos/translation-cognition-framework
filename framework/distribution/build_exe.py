"""Gera o .exe de um clique. Uso: build_exe.py <dist_do_pacote> [saida_dir] (nome do exe vem do manifest.json).
Sem saida_dir, grava em <projeto>/output (ignorada no git). Nunca dentro de dist/: o PyInstaller embute o dist inteiro."""
import json
import pathlib
import subprocess
import sys
import tempfile

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
dist = pathlib.Path(sys.argv[1]).resolve()
saida = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else dist.parent / 'output'
if dist in (saida, *saida.parents):  # nao 'assert': some com python -O
    raise AssertionError('saida dentro de dist/ seria embutida no proprio exe')
nome = json.loads((dist / 'manifest.json').read_text(encoding='utf-8'))['app']['exe']
ico = [f'--icon={dist / "icone.ico"}'] if (dist / 'icone.ico').is_file() else []
with tempfile.TemporaryDirectory() as work:  # work/spec do PyInstaller fora da pasta de saida
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--onefile', '--windowed', *ico, '--name', nome,
                    '--add-data', f'{dist};.',
                    '--distpath', str(saida), '--workpath', work, '--specpath', work,
                    str(pathlib.Path(__file__).parent / 'patcher.py')], check=True, capture_output=True)
print(saida / (nome + '.exe'))
