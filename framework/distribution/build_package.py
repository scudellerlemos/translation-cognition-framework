"""Gera o pacote do patcher: deltas bsdiff + manifest.json. Uso: build_package.py <distribution.json> <source_dat> <output> <dist> <versao> [arte.webp|png [capa.jpg]]
So entram arquivos de output/ que existem em source_dat e diferem dele (sondas de teste ficam de fora)."""
import hashlib
import json
import pathlib
import sys

import bsdiff4


def _grava(p, dados):
    """tmp + replace: build que cai no meio nao deixa delta/manifest truncado no pacote."""
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_bytes(dados)
    tmp.replace(p)


if len(sys.argv) < 6 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
cfg = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
src, out, dist = map(pathlib.Path, sys.argv[2:5])
versao, arte = sys.argv[5], sys.argv[6:]
(dist / 'deltas').mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
files = []
for f in sorted(out.glob(cfg['padrao_arquivos'])):
    if not (src / f.name).is_file():
        continue
    a, b = (src / f.name).read_bytes(), f.read_bytes()
    if a == b:
        continue
    d = bsdiff4.diff(a, b)
    assert bsdiff4.patch(a, d) == b, f.name
    _grava(dist / 'deltas' / (f.name + '.bsdiff'), d)
    files.append({'name': f.name, 'sha_original': sha(a), 'sha_final': sha(b)})
_grava(dist / 'manifest.json', json.dumps({'version': versao, 'app': cfg, 'files': files}, indent=1).encode('utf-8'))
if arte:  # arte do painel lateral: 320x480, PNG (o tkinter nao le webp), com o titulo. Fica so no pacote, nunca no repo
    from PIL import Image, ImageDraw, ImageFont
    W, H = 640, 960  # desenha em 2x e reduz, para o texto sair suave
    img = Image.open(arte[0]).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    veu = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veu)
    for y in range(H - 420, H):  # degrade branco embaixo: garante a leitura do texto sobre a nevoa
        vd.line([(0, y), (W, y)], fill=(245, 247, 252, int(235 * (y - (H - 420)) / 420)))
    img = Image.alpha_composite(img, veu)
    def fonte(nome, tam):
        try:
            return ImageFont.truetype(nome, tam)
        except OSError:
            return ImageFont.load_default(tam)
    d = ImageDraw.Draw(img)
    for texto, nome, tam, cor, y in (('PATCH TRADUÇÃO', 'segoeuib.ttf', 34, (58, 79, 168), H - 255),
                                     (cfg['titulo_curto'], 'segoeuib.ttf', 70, (31, 42, 92), H - 205),
                                     (f"by {cfg['autor']}", 'segoeui.ttf', 38, (91, 99, 133), H - 110)):
        d.text((W // 2, y), texto, font=fonte(nome, tam), fill=cor, anchor='mt')
    img.convert('RGB').resize((320, 480), Image.LANCZOS).save(dist / 'arte.png')
    if len(arte) > 1:  # recorte de rosto da capa (icone_recorte); sem a capa, recorta o rosto da propria arte
        ic = Image.open(arte[1]).convert('RGBA').crop(tuple(cfg['icone_recorte'])).resize((512, 512), Image.LANCZOS)
    else:
        ic = Image.open(arte[0]).convert('RGBA').crop((300, 440, 800, 940)).resize((512, 512), Image.LANCZOS)
    mask = Image.new('L', (512, 512), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 511, 511), radius=100, fill=255)
    ic.putalpha(mask)
    ImageDraw.Draw(ic).rounded_rectangle((6, 6, 505, 505), radius=96, outline=(31, 42, 92, 255), width=12)
    ic.save(dist / 'icone.ico', sizes=[(n, n) for n in (16, 24, 32, 48, 64, 128, 256)])
print(f'{len(files)} arquivos, versao {versao}, pacote em {dist}')
