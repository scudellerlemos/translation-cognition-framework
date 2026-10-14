"""Patcher generico de traducao (identidade do jogo vem do manifest.json, bloco 'app'). Uso: patcher [instalar|verificar|desinstalar] [--jogo <pasta DAT>] [--pacote <pasta>]
Sem argumento, instala (o .exe de um clique). So altera arquivo cujo hash bate com o original do manifesto."""
import hashlib
import json
import pathlib
import shutil
import sys

import bsdiff4

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def achar_jogo(app):
    raiz = pathlib.Path('C:/Program Files (x86)/Steam/steamapps/common')  # ponytail: so a biblioteca padrao; outras via --jogo
    for d in raiz.glob(f"{app['pasta_glob']}/{app['subpasta']}"):
        return d


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


def estado(jogo, f):
    g = jogo / f['name']
    if not g.is_file():
        return 'ausente'
    h = sha(g)
    return 'original' if h == f['sha_original'] else 'traduzido' if h == f['sha_final'] else 'desconhecido'


def instalar(jogo, pkg, man):
    if jogo_aberto(man['app']):
        return print(aviso_aberto(man['app'])) or 1
    plano = []
    for f in man['files']:
        s = estado(jogo, f)
        if s == 'traduzido':
            continue
        if s != 'original':
            return print(f"{f['name']}: {s} (jogo atualizado ou modificado). Nada foi alterado. "
                         "Use 'verificar arquivos' da Steam e rode de novo.") or 1
        plano.append(f)
    print(f'{len(plano)} arquivo(s) a traduzir, {len(man["files"]) - len(plano)} ja em dia.')
    feitos = []
    try:
        for f in plano:
            g = jogo / f['name']
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
        print('Falha:', e, '- restaurando.')
        for f in feitos:
            shutil.copy2(jogo / (f['name'] + '.bak'), jogo / f['name'])
        return 1
    print('Tradução instalada. Backups em *.bak na pasta do jogo.')


def desinstalar(jogo, man):
    if jogo_aberto(man['app']):
        return print(aviso_aberto(man['app'])) or 1
    n = 0
    for f in man['files']:
        g, bak = jogo / f['name'], jogo / (f['name'] + '.bak')
        if estado(jogo, f) == 'traduzido':
            if not bak.is_file() or sha(bak) != f['sha_original']:
                return print(f"{f['name']}: sem backup valido. Use 'verificar arquivos' da Steam.") or 1
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
        return print('Pasta do jogo nao encontrada. Rode com --jogo "<pasta do jogo>".') or 1
    print(f"Tradução para {man['app']['idioma']} v{man['version']} - jogo em {jogo}")
    return {'instalar': lambda: instalar(jogo, pkg, man), 'desinstalar': lambda: desinstalar(jogo, man),
            'verificar': lambda: verificar(jogo, man)}[cmd]()


def resolver_pasta(p, man):
    """Aceita a pasta do jogo, a DAT ou a english/DAT; devolve a que tem os arquivos do jogo."""
    p = pathlib.Path(p)
    for c in (p, p / pathlib.Path(man['app']['subpasta']).name, p / man['app']['subpasta']):
        if (c / man['files'][0]['name']).is_file():
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
    root.geometry('820x480')
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

    lbl(f, app['titulo'], font=('Segoe UI', 20, 'bold'), fg=TXT).pack(fill='x')
    lbl(f, f"Tradução para {app['idioma']}  ·  v{man['version']}  ·  by {app['autor']}", font=('Segoe UI', 10), fg=SUB).pack(fill='x', pady=(0, 14))

    aviso = tk.Frame(f, bg='#fff1cc', padx=12, pady=8)
    aviso.pack(fill='x')
    for i, t in enumerate(app['aviso']):
        lbl(aviso, t, font=('Segoe UI', 10, 'bold') if i == 0 else ('Segoe UI', 9), fg='#7a4b00', bg='#fff1cc').pack(fill='x')

    lbl(f, '1. Onde o jogo está instalado?', font=('Segoe UI', 11, 'bold'), fg=TXT).pack(fill='x', pady=(16, 4))
    linha = tk.Frame(f, bg=BG)
    linha.pack(fill='x')
    achado = achar_jogo(app)
    caminho = tk.StringVar(value=str(achado.parent.parent if achado else ''))  # raiz do jogo, nao a english/DAT
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
            msg('Os arquivos do jogo não são os esperados (outra versão ou já modificados). Na Steam, use "Verificar integridade dos arquivos" e tente de novo.', 'aviso')

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
        finally:
            sys.stdout = old
        atualizar()
        if r:
            messagebox.showerror('Algo deu errado', falha + '\nNada foi deixado pela metade. Veja os detalhes na janela.')
            mostrar.set(True)
            alternar()
        else:
            messagebox.showinfo('Pronto!', ok)

    def alternar():
        if mostrar.get():
            log.pack(fill='x', pady=(6, 0))
        else:
            log.pack_forget()

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
