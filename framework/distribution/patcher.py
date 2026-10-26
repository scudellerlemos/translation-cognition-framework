"""Patcher generico de traducao (identidade do jogo vem do manifest.json, bloco 'app'). Uso: patcher [instalar|verificar|desinstalar] [--jogo <pasta DAT>] [--pacote <pasta>]
Sem argumento, instala (o .exe de um clique). So altera arquivo cujo hash bate com o original do manifesto."""
import hashlib
import json
import pathlib
import re
import shutil
import sys
import tempfile

import bsdiff4

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def bibliotecas_steam(vdf=None):
    """Pastas steamapps/common de todas as bibliotecas da Steam: a padrao, a do registro e as de libraryfolders.vdf."""
    raizes = [pathlib.Path('C:/Program Files (x86)/Steam')]
    if vdf is None:
        try:
            import winreg
            for hive, chave, nome in ((winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam', 'SteamPath'),
                                      (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Valve\Steam', 'InstallPath')):
                try:
                    with winreg.OpenKey(hive, chave) as k:
                        raizes.append(pathlib.Path(winreg.QueryValueEx(k, nome)[0]))
                except OSError:
                    pass
        except ImportError:  # fora do Windows
            pass
        vdf = next((r / 'steamapps' / 'libraryfolders.vdf' for r in raizes if (r / 'steamapps' / 'libraryfolders.vdf').is_file()), None)
    if vdf and pathlib.Path(vdf).is_file():
        texto = pathlib.Path(vdf).read_text(encoding='utf-8', errors='replace')
        raizes += [pathlib.Path(m.replace('\\\\', '\\')) for m in re.findall(r'"path"\s+"([^"]+)"', texto)]
    vistos, saida = set(), []
    for r in raizes:
        c = r / 'steamapps' / 'common'
        chave = str(c).replace('\\', '/').lower()  # 'C:\x' e 'C:/x' sao a mesma pasta (e a mesma entrada fora do Windows)
        if chave not in vistos:
            vistos.add(chave)
            saida.append(c)
    return saida


def achar_jogo(app, bibliotecas=None):
    for raiz in bibliotecas if bibliotecas is not None else bibliotecas_steam():
        for d in raiz.glob(f"{app['pasta_glob']}/{app['subpasta']}"):
            return d


def preflight(jogo, plano):
    """Antes de tocar em qualquer arquivo: espaco para o .bak + .novo e permissao de escrita. Devolve a frase de erro ou None."""
    try:
        with tempfile.TemporaryFile(dir=jogo):
            pass
    except OSError as e:
        return falha_amigavel(PermissionError(e))
    precisa = 2 * sum(alvo(jogo, f).stat().st_size for f in plano)
    if shutil.disk_usage(jogo).free < precisa:
        return falha_amigavel(OSError(28, 'sem espaco'))


def jogo_aberto(app):
    """True se o jogo (ou o launcher) esta rodando: com ele aberto os arquivos ficam bloqueados."""
    import subprocess
    for exe in app['processos']:
        r = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {exe}', '/NH'], capture_output=True, text=True, errors='replace',
                           creationflags=0x08000000)  # sem janela de console
        if exe.lower() in (r.stdout or '').lower():
            return True
    return False


aviso_aberto = lambda app: f"O jogo está aberto. Feche o {app['titulo']} (e o launcher) e tente de novo."


def alvo(jogo, f):
    """Arquivo do jogo que o delta `f` altera: `path` (relativo a pasta do jogo) ou, sem ele, o proprio `name`."""
    return jogo / f.get('path', f['name'])


def estado(jogo, f):
    g = alvo(jogo, f)
    if not g.is_file():
        return 'ausente'
    h = sha(g)
    return 'original' if h == f['sha_original'] else 'traduzido' if h == f['sha_final'] else 'desconhecido'


def motivo(f, s):
    """Explica em linguagem de usuario por que o arquivo `f`, no estado `s`, nao serve."""
    if s == 'ausente':
        return (f"Não encontrei o arquivo {f['name']} nessa pasta. Confira se é a pasta certa do jogo "
                "e se a instalação dele está completa.")
    return (f"O arquivo {f['name']} do jogo é diferente do esperado. Isso acontece quando já existe outra tradução ou "
            "mod instalado, ou quando o jogo foi atualizado. Na Steam, use 'Verificar integridade dos arquivos' "
            "e rode este instalador de novo.")


def falha_amigavel(e):
    """Traduz uma excecao da instalacao em uma frase que o usuario final entende."""
    if isinstance(e, PermissionError):
        return ("O Windows não deixou alterar os arquivos do jogo. Feche o jogo e programas que possam estar usando a "
                "pasta (o antivírus, por exemplo) ou abra este instalador como administrador.")
    if isinstance(e, FileNotFoundError):
        return "Falta um arquivo dentro deste instalador. Baixe o instalador de novo."
    if isinstance(e, OSError) and e.errno == 28:
        return "Não há espaço livre suficiente no disco. Libere espaço e tente de novo."
    return "Não consegui montar a tradução (o instalador pode estar corrompido). Baixe o instalador de novo."


def instalar(jogo, pkg, man):
    if jogo_aberto(man['app']):
        return print(aviso_aberto(man['app'])) or 1
    plano = []
    for f in man['files']:
        s = estado(jogo, f)
        if s == 'traduzido':
            continue
        if s != 'original':
            return print(motivo(f, s), 'Nada foi alterado no seu jogo.') or 1
        plano.append(f)
    if plano and (erro := preflight(jogo, plano)):
        return print(erro, 'Nada foi alterado no seu jogo.') or 1
    print(f'{len(plano)} arquivo(s) a traduzir, {len(man["files"]) - len(plano)} ja em dia.')
    feitos = []
    try:
        for f in plano:
            g = alvo(jogo, f)
            bak = g.with_name(g.name + '.bak')
            if not bak.exists() or sha(bak) != f['sha_original']:  # g ja foi conferido como original
                shutil.copy2(g, bak)
            novo = bsdiff4.patch(g.read_bytes(), (pkg / 'deltas' / (f['name'] + '.bsdiff')).read_bytes())
            tmp = g.with_name(g.name + '.novo')
            tmp.write_bytes(novo)
            if sha(tmp) != f['sha_final']:
                tmp.unlink()
                raise RuntimeError(f"{f['name']}: resultado com hash errado")
            tmp.replace(g)
            feitos.append(f)
    except Exception as e:  # volta tudo ao original: nunca deixa o jogo em estado misto
        print(falha_amigavel(e), 'Os arquivos do jogo foram devolvidos ao original.')
        for f in feitos:
            g = alvo(jogo, f)
            shutil.copy2(g.with_name(g.name + '.bak'), g)
        return 1
    print('Tradução instalada. Backups em *.bak na pasta do jogo.')


def desinstalar(jogo, man):
    if jogo_aberto(man['app']):
        return print(aviso_aberto(man['app'])) or 1
    n = 0
    for f in man['files']:
        g = alvo(jogo, f)
        bak = g.with_name(g.name + '.bak')
        if estado(jogo, f) == 'traduzido':
            if not bak.is_file() or sha(bak) != f['sha_original']:
                return print(f"Não achei a cópia de segurança de {f['name']} para desfazer a tradução. "
                             "Na Steam, use 'Verificar integridade dos arquivos' para voltar ao original.") or 1
            shutil.copy2(bak, g)
            n += 1
    print(f'{n} arquivo(s) restaurados ao original.')


def verificar(jogo, man):
    c = {}
    for f in man['files']:
        c[estado(jogo, f)] = c.get(estado(jogo, f), 0) + 1
    print(c)


def main():
    a = sys.argv[1:]
    if '-h' in a or '--help' in a:
        return print(__doc__)
    arg = lambda k: pathlib.Path(a[a.index(k) + 1]) if k in a else None
    cmd = a[0] if a and not a[0].startswith('--') else 'instalar'
    pkg = arg('--pacote') or pathlib.Path(getattr(sys, '_MEIPASS', pathlib.Path(__file__).parent / 'dist'))
    man = json.loads((pkg / 'manifest.json').read_text(encoding='utf-8'))
    jogo = arg('--jogo') or achar_jogo(man['app'])
    if not jogo or not jogo.is_dir():
        return print('Não encontrei o jogo instalado. Rode com --jogo "<pasta do jogo>".') or 1
    print(f"Tradução para {man['app']['idioma']} v{man['version']} - jogo em {jogo}")
    return {'instalar': lambda: instalar(jogo, pkg, man), 'desinstalar': lambda: desinstalar(jogo, man),
            'verificar': lambda: verificar(jogo, man)}[cmd]()


def resolver_pasta(p, man):
    """Aceita a pasta do jogo, a DAT ou a english/DAT; devolve a que tem os arquivos do jogo."""
    p = pathlib.Path(p)
    for c in (p, p / pathlib.Path(man['app']['subpasta']).name, p / man['app']['subpasta']):
        if alvo(c, man['files'][0]).is_file():
            return c


def gui():
    import io
    import tkinter as tk
    from tkinter import filedialog, messagebox

    BG, AZUL, TXT, SUB = '#f5f7fc', '#3a4fa8', '#1f2a5c', '#5b6385'
    pkg = pathlib.Path(getattr(sys, '_MEIPASS', pathlib.Path(__file__).parent / 'dist'))
    man = json.loads((pkg / 'manifest.json').read_text(encoding='utf-8'))
    root = tk.Tk()
    app = man['app']
    root.title(f"Patch Tradução {app['titulo_curto']} - by {app['autor']}")
    ALTURA = 480
    root.geometry(f'820x{ALTURA}')
    root.resizable(False, False)
    root.configure(bg=BG)
    if (pkg / 'icone.ico').is_file():
        root.iconbitmap(str(pkg / 'icone.ico'))
    arte = pkg / 'arte.png'
    if arte.is_file():
        img = tk.PhotoImage(file=str(arte))
        tk.Label(root, image=img, bd=0).pack(side='left', fill='y')
        root.img = img  # mantem a referencia viva
    f = tk.Frame(root, bg=BG, padx=26, pady=22)
    f.pack(side='left', fill='both', expand=True)
    lbl = lambda parent, t, **k: tk.Label(parent, text=t, bg=k.pop('bg', BG), anchor='w', justify='left', **k)

    lbl(f, app['titulo'], font=('Segoe UI', 20, 'bold'), fg=TXT, wraplength=448).pack(fill='x')
    lbl(f, f"Tradução para {app['idioma']}  ·  v{man['version']}  ·  by {app['autor']}", font=('Segoe UI', 10), fg=SUB).pack(fill='x', pady=(0, 14))

    aviso = tk.Frame(f, bg='#fff1cc', padx=12, pady=8)
    aviso.pack(fill='x')
    for i, t in enumerate(app['aviso']):
        lbl(aviso, t, font=('Segoe UI', 10, 'bold') if i == 0 else ('Segoe UI', 9), fg='#7a4b00', bg='#fff1cc').pack(fill='x')

    lbl(f, '1. Onde o jogo está instalado?', font=('Segoe UI', 11, 'bold'), fg=TXT).pack(fill='x', pady=(16, 4))
    linha = tk.Frame(f, bg=BG)
    linha.pack(fill='x')
    achado = achar_jogo(app)
    raiz = achado
    for _ in pathlib.Path(app['subpasta']).parts:  # raiz do jogo = achado menos os niveis da subpasta ('.' = nenhum)
        raiz = raiz.parent if raiz else raiz
    caminho = tk.StringVar(value=str(raiz or ''))
    tk.Entry(linha, textvariable=caminho, font=('Segoe UI', 9), relief='solid', bd=1).pack(side='left', fill='x', expand=True, ipady=4)
    btn = lambda parent, t, cmd, **k: tk.Button(parent, text=t, command=cmd, relief='flat', cursor='hand2', font=('Segoe UI', 10, 'bold'),
                                               **{'padx': 14, 'pady': 6, **k})
    status = tk.StringVar()
    cor = {'ok': '#1b7a3a', 'aviso': '#b00020', 'info': TXT}
    lbl_status = lbl(f, '', textvariable=status, font=('Segoe UI', 10), fg=TXT, wraplength=440)
    lbl_status.pack(fill='x', pady=(8, 0))

    lbl(f, '2. Instalar', font=('Segoe UI', 11, 'bold'), fg=TXT).pack(fill='x', pady=(16, 6))
    botoes = tk.Frame(f, bg=BG)
    botoes.pack(fill='x')

    log = tk.Text(f, height=6, state='disabled', wrap='word', font=('Consolas', 9), relief='solid', bd=1)
    mostrar = tk.BooleanVar(value=False)

    def escrever(t):
        log.config(state='normal')
        log.insert('end', t)
        log.see('end')
        log.config(state='disabled')
        root.update_idletasks()

    class Saida(io.TextIOBase):
        def write(self, t):
            escrever(t)
            return len(t)

    def msg(t, tipo='info'):
        status.set(t)
        lbl_status.config(fg=cor[tipo])
        root.update_idletasks()

    def pasta():
        j = resolver_pasta(caminho.get(), man) if caminho.get() else None
        if not j:
            msg('Não encontrei o jogo nessa pasta. Escolha a pasta de instalação do jogo (dentro de steamapps/common).', 'aviso')
        return j

    def atualizar():
        j = pasta()
        if not j:
            return
        c = {}
        for x in man['files']:
            c[estado(j, x)] = c.get(estado(j, x), 0) + 1
        n = len(man['files'])
        if c == {'original': n}:
            msg('Jogo encontrado e pronto para receber a tradução.', 'ok')
        elif c == {'traduzido': n}:
            msg('A tradução já está instalada neste jogo.', 'ok')
        else:
            ruim = next(x for x in man['files'] if estado(j, x) not in ('original', 'traduzido'))
            msg(motivo(ruim, estado(j, ruim)), 'aviso')

    def procurar():
        d = filedialog.askdirectory(title=f"Pasta de instalação do {app['titulo']} (Steam)", initialdir=caminho.get() or None)
        if d:
            caminho.set(str(pathlib.Path(d)))
            atualizar()

    def rodar(fn, ok, falha):
        j = pasta()
        if not j:
            return
        if jogo_aberto(app):
            msg(aviso_aberto(app), 'aviso')
            return messagebox.showwarning('Feche o jogo', aviso_aberto(app))
        msg('Trabalhando... aguarde.')
        old, sys.stdout = sys.stdout, Saida()
        try:
            r = fn(j)
        except Exception as e:
            r = print(falha_amigavel(e)) or 1
        finally:
            sys.stdout = old
        atualizar()
        if r:
            messagebox.showerror('Algo deu errado', falha + '\n\n' + (log.get('1.0', 'end').strip().splitlines() or [''])[-1])
            mostrar.set(True)
            alternar()
        else:
            messagebox.showinfo('Pronto!', ok)

    def alternar():
        if mostrar.get():
            if not log.get('1.0', 'end').strip():
                escrever('Nada para mostrar ainda. Aqui aparece o passo a passo quando você instalar ou voltar ao original.\n')
            root.geometry(f'820x{ALTURA + 150}')
            log.pack(fill='x', pady=(6, 0))
        else:
            log.pack_forget()
            root.geometry(f'820x{ALTURA}')

    def detalhes():
        mostrar.set(not mostrar.get())
        alternar()

    btn(linha, 'Procurar...', procurar, bg='#e3e8f7', fg=TXT).pack(side='left', padx=(6, 0))
    btn(botoes, 'Instalar tradução', lambda: rodar(lambda j: instalar(j, pkg, man), 'Tradução instalada! Abra o jogo normalmente pela Steam.',
                                                  'Não foi possível instalar.'), bg=AZUL, fg='white', padx=22).pack(side='left')
    btn(botoes, 'Voltar ao original', lambda: rodar(lambda j: desinstalar(j, man), 'O jogo voltou ao original.',
                                                   'Não foi possível desinstalar.'), bg='#e3e8f7', fg=TXT).pack(side='left', padx=8)
    tk.Button(f, text='Mostrar detalhes', command=detalhes, relief='flat', bd=0, bg=BG, fg=SUB, cursor='hand2', font=('Segoe UI', 9, 'underline')).pack(anchor='w', pady=(10, 0))
    lbl(f, 'Se a Steam atualizar o jogo ou verificar os arquivos, rode o instalador de novo.', font=('Segoe UI', 8), fg=SUB, wraplength=440).pack(side='bottom', fill='x')
    atualizar()
    root.mainloop()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        gui()
        sys.exit(0)
    sys.exit(main() or 0)
