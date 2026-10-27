"""Testa o .exe do patcher como um usuario sem Python: jogo falso fora da Steam, ambiente esvaziado.
Uso: verificar_exe.py <exe> <dist_do_pacote> <pasta_dos_originais>   (sai 0 se tudo passou)
O .exe e sem janela de console: confere codigo de saida e hash dos arquivos, nao o texto impresso."""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

if len(sys.argv) != 4 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
exe, dist, orig = (pathlib.Path(a).resolve() for a in sys.argv[1:])
man = json.loads((dist / 'manifest.json').read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
env = {k: v for k, v in os.environ.items() if k.upper() in ('SYSTEMROOT', 'WINDIR', 'COMSPEC', 'TEMP', 'TMP', 'USERPROFILE')}
env['PATH'] = os.path.join(env.get('SYSTEMROOT', r'C:\Windows'), 'System32')  # sem Python no PATH
falhas = []


def confere(nome, cond):
    print(('ok   ' if cond else 'FALHOU ') + nome)
    if not cond:
        falhas.append(nome)


def rodar(*args):
    return subprocess.run([str(exe), *args], env=env, capture_output=True, timeout=300).returncode


def gravar(p, dados):
    """Grava via arquivo temporario + replace (nunca deixa meio arquivo)."""
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_bytes(dados if isinstance(dados, bytes) else dados.encode('utf-8'))
    tmp.replace(p)


def estados(jogo, chave):
    return [sha(jogo / f.get('path', f['name'])) == f[chave] for f in man['files']]


with tempfile.TemporaryDirectory() as tmp:
    jogo = pathlib.Path(tmp) / 'Biblioteca fora da Steam' / 'Jogo'
    # lista explicita no distribution.json (app.arquivos) ou, nos projetos de padrao (*.DAT), os files do manifesto
    pares = ([(a['path'], a['original']) for a in man['app']['arquivos']] if 'arquivos' in man['app']
             else [(f.get('path', f['name']), f['name']) for f in man['files']])
    for destino, original in pares:
        alvo = jogo / destino
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(orig / original, alvo)
    confere('jogo falso nasce original', all(estados(jogo, 'sha_original')))
    confere('instalar sai 0', rodar('instalar', '--jogo', str(jogo)) == 0)
    confere('arquivos ficam traduzidos (hash final)', all(estados(jogo, 'sha_final')))
    confere('instalar de novo e idempotente', rodar('instalar', '--jogo', str(jogo)) == 0 and all(estados(jogo, 'sha_final')))
    confere('desinstalar sai 0', rodar('desinstalar', '--jogo', str(jogo)) == 0)
    confere('volta byte a byte ao original', all(estados(jogo, 'sha_original')))
    gravar(jogo / man['files'][0].get('path', man['files'][0]['name']), b'outra versao do jogo')
    confere('arquivo estranho: recusa (saida 1) sem alterar', rodar('instalar', '--jogo', str(jogo)) == 1
            and (jogo / man['files'][0].get('path', man['files'][0]['name'])).read_bytes() == b'outra versao do jogo')
    confere('pasta errada: recusa (saida 1)', rodar('instalar', '--jogo', str(pathlib.Path(tmp) / 'nao existe')) == 1)

p = subprocess.Popen([str(exe)], env=env)  # sem argumento abre a janela (tkinter, icone, arte)
time.sleep(6)
confere('janela abre e fica de pe', p.poll() is None)
p.kill()
sys.exit(1 if falhas else 0)
