"""Pagina local de revisao humana das planilhas de qa_revisao/para_revisar (HTML, fora do git).

A pagina so LE os CSVs embutidos e devolve o mesmo CSV (mesmas colunas, BOM) com o que o humano digitou; nao
preenche nada sozinha. Codigos de controle `[xx]` aparecem esmaecidos (a fala codificada, nao a limpa).
Com `--serve` o botao Salvar grava direto na pasta (o seletor de arquivo do navegador falha em alguns setups).

  python review_page.py <projeto> [--serve] [--port 8765]
"""
import argparse
import csv
import http.server
import json
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402
from review_page_tpl import PAGE  # noqa: E402

# planilha -> colunas que o humano edita
SHEETS = {"escalonamento.csv": ["alias", "correcao"], "onda_amostra.csv": [],
          "amostra_qualidade.csv": ["veredito", "nota"]}


def load(box: Path) -> dict:
    data = {}
    for name, edit in SHEETS.items():
        p = box / name
        if p.exists():
            with p.open(encoding="utf-8-sig", newline="") as fh:
                rd = csv.DictReader(fh)
                data[name] = {"cols": rd.fieldnames, "edit": edit, "rows": list(rd)}
    return data


def render(box: Path) -> str:
    return PAGE.replace("__DATA__", json.dumps(load(box), ensure_ascii=False).replace("</", "<\\/"))


def save(box: Path, name: str, body: bytes) -> bool:
    """Grava so planilha editavel conhecida (nome vindo da URL nunca vira caminho)."""
    if not SHEETS.get(name):
        return False
    paths.atomic_write(box / name, body)      # planilha do revisor: queda no meio nao a trunca
    return True


def serve(box: Path, port: int) -> None:
    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(render(box).encode("utf-8"))

        def do_POST(self):
            ok = save(box, self.path.removeprefix("/save/"), self.rfile.read(int(self.headers["Content-Length"])))
            self.send_response(200 if ok else 400)
            self.end_headers()

        def log_message(self, *a):
            pass

    print(f"http://127.0.0.1:{port}  (Ctrl+C para parar)")
    webbrowser.open(f"http://127.0.0.1:{port}")
    http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("project")
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    box = paths.qa_outbox(paths.require_project(a.project))
    box.mkdir(parents=True, exist_ok=True)
    out = box / "revisar.html"
    out.write_text(render(box), encoding="utf-8")
    counts = ", ".join(f"{k}: {len(v['rows'])}" for k, v in load(box).items())
    print(f"{out}  ({counts})")
    if a.serve:
        serve(box, a.port)


if __name__ == "__main__":
    main()
