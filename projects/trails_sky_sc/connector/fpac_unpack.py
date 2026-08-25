#!/usr/bin/env python3
"""fpac_unpack.py — lê o índice de um contêiner FPAC (formato Falcom, ver table_schema.md).

Camada 0 (contêiner) apenas. NÃO decodifica o script interno `#scp` dos arquivos scena/*.dat
(camada 1, ainda não mapeada — ver table_schema.md).

Uso:
  python fpac_unpack.py <arquivo.pac>              # lista entradas
  python fpac_unpack.py <arquivo.pac> --extract-to <dir>   # extrai todos os arquivos
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

HEADER = struct.Struct("<4sIII")
ENTRY = struct.Struct("<IIQQQ")


def read_index(path: Path) -> tuple[bytes, list[tuple[str, int, int, int]]]:
    data = path.read_bytes()
    magic, count, first_addr, unk = HEADER.unpack_from(data, 0)
    if magic != b"FPAC":
        raise ValueError(f"magic invalido: {magic!r} (esperado b'FPAC')")
    entries = []
    off = HEADER.size
    for _ in range(count):
        crc, pad, name_addr, size, data_addr = ENTRY.unpack_from(data, off)
        off += ENTRY.size
        name_end = data.index(b"\x00", name_addr)
        name = data[name_addr:name_end].decode("ascii")
        entries.append((name, size, data_addr, crc))
    return data, entries


def extract_all(path: Path, out_dir: Path) -> None:
    data, entries = read_index(path)
    for name, size, addr, _crc in entries:
        dest = out_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data[addr:addr + size])


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    path = Path(args[0])
    if "--extract-to" in args:
        out_dir = Path(args[args.index("--extract-to") + 1])
        extract_all(path, out_dir)
        print(f"extraido para {out_dir}")
        return
    _data, entries = read_index(path)
    print(f"{path.name}: {len(entries)} entradas")
    for name, size, addr, _crc in entries:
        print(f"  {name}\tsize={size}\taddr={addr}")


def _demo() -> None:
    """Self-check: monta um FPAC minimo em memoria (2 arquivos) e confere round-trip do indice."""
    import tempfile

    names = [b"foo.dat", b"bar/baz.dat"]
    contents = [b"hello", b"world!!"]

    name_table = b"\x00".join(names) + b"\x00"
    name_offsets = []
    pos = 0
    for n in names:
        name_offsets.append(pos)
        pos += len(n) + 1

    header_size = HEADER.size
    entries_size = ENTRY.size * len(names)
    name_table_addr = header_size + entries_size
    data_start = name_table_addr + len(name_table)

    data_blobs = b""
    data_addrs = []
    pos = data_start
    for c in contents:
        data_addrs.append(pos)
        data_blobs += c
        pos += len(c)

    entries_bytes = b""
    for i, n in enumerate(names):
        entries_bytes += ENTRY.pack(
            0, 0, name_table_addr + name_offsets[i], len(contents[i]), data_addrs[i]
        )

    blob = HEADER.pack(b"FPAC", len(names), data_start, 1) + entries_bytes + name_table + data_blobs

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "test.pac"
        p.write_bytes(blob)
        _data, entries = read_index(p)
        assert [e[0] for e in entries] == ["foo.dat", "bar/baz.dat"], entries
        assert [e[1] for e in entries] == [5, 7], entries
        out = Path(td) / "out"
        extract_all(p, out)
        assert (out / "foo.dat").read_bytes() == b"hello"
        assert (out / "bar" / "baz.dat").read_bytes() == b"world!!"
    print("fpac_unpack self-check OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        _demo()
    else:
        main()
