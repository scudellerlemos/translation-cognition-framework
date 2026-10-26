"""Gera artifacts/ordem_cenas.txt (um id de cena por linha, ordem do jogo) a partir de ENG/DataBase.sdat:EventManagerData.bin.
Uso: python extrai_ordem.py projects/<nome> "<pasta Data do jogo>"   (conector utawarerumono; 433 registros de 48 bytes, chave de evento = campo 3)"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "framework" / "runtime"))
from paths import atomic_write  # noqa: E402

proj, data = Path(sys.argv[1]), Path(sys.argv[2])
d = (data / "ENG" / "DataBase.sdat").read_bytes()
pk = d.index(b"Pack        "); n = struct.unpack_from("<I", d, pk + 16)[0]
nomes = d[16 + struct.unpack_from("<I", d, 16)[0]:pk].rstrip(b"\0").split(b"\0")
o, s = struct.unpack_from("<II", d, pk + 20 + 8 * nomes.index(b"EventManagerData.bin"))
b = d[o:o + s]
cenas = {p.name for p in (proj / "artifacts" / "scenes").iterdir() if p.name[0].isdigit()}
ordem = []
for i in range(struct.unpack_from("<I", b, 0)[0]):
    k = struct.unpack_from("<12I", b, 4 + 48 * i)[3]
    sid = f"{k // 100000:02d}_{k // 1000 % 100:02d}_{k % 1000 // 10:02d}"
    if sid in cenas and sid not in ordem: ordem.append(sid)
atomic_write(proj / "artifacts" / "ordem_cenas.txt", "\n".join(ordem) + "\n", newline="\n")
print(len(ordem), "de", len(cenas), "cenas; fora da lista:", sorted(cenas - set(ordem))[:20])
