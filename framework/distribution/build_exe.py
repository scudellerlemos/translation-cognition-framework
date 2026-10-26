"""Gera o .exe de um clique. Uso: build_exe.py <dist_do_pacote> [saida_dir] (nome do exe vem do manifest.json).
Sem saida_dir, grava em <projeto>/output (ignorada no git). Nunca dentro de dist/: o PyInstaller embute o dist inteiro."""
import hashlib
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
man = json.loads((dist / 'manifest.json').read_text(encoding='utf-8'))
nome, app = man['app']['exe'], man['app']
ico = [f'--icon={dist / "icone.ico"}'] if (dist / 'icone.ico').is_file() else []


def gravar(p, dados):
    """Grava via arquivo temporario + replace (nunca deixa meio arquivo)."""
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_bytes(dados if isinstance(dados, bytes) else dados.encode('utf-8'))
    tmp.replace(p)


def versao(v):
    """Arquivo de versao do Windows (propriedades do .exe): sem ele o SmartScreen e os antivirus desconfiam mais."""
    n = (tuple(int(x) for x in v.split('.')) + (0, 0, 0, 0))[:4]
    s = lambda k, x: f"StringStruct('{k}', {x!r})"
    return (f"VSVersionInfo(ffi=FixedFileInfo(filevers={n}, prodvers={n}, mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),\n"
            f" kids=[StringFileInfo([StringTable('040904B0', [{s('CompanyName', app['autor'])}, "
            f"{s('FileDescription', 'Patch de traducao ' + app['titulo_curto'])}, {s('FileVersion', v)}, "
            f"{s('InternalName', nome)}, {s('OriginalFilename', nome + '.exe')}, "
            f"{s('ProductName', 'Traducao ' + app['titulo'])}, {s('ProductVersion', v)}])]), VarFileInfo([VarStruct('Translation', [1033, 1200])])])\n")


with tempfile.TemporaryDirectory() as work:  # work/spec do PyInstaller fora da pasta de saida
    vf = pathlib.Path(work) / 'versao.txt'
    gravar(vf, versao(man['version']))
    r = subprocess.run([sys.executable, '-m', 'PyInstaller', '--onefile', '--windowed', f'--version-file={vf}', *ico, '--name', nome,
                    '--add-data', f'{dist};.',
                    '--distpath', str(saida), '--workpath', work, '--specpath', work,
                    str(pathlib.Path(__file__).parent / 'patcher.py')], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])
exe = saida / (nome + '.exe')
print(exe)
print('SHA-256', hashlib.sha256(exe.read_bytes()).hexdigest(), '(publicar na release)')
