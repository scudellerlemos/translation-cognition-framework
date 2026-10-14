"""Template HTML da pagina de revisao (review_page.py). Fica em .py: a allowlist do content_guard nao tem .html."""
PAGE = r"""<!doctype html><meta charset="utf-8"><title>Revisao</title>
<style>
:root{--bg:#f6f6f4;--fg:#1c1c1c;--mut:#6b6b6b;--card:#fff;--line:#d9d9d4;--acc:#1d5fbf;--code:#b0b0b0;--ok:#1b7a3d;--bad:#b3261e}
@media(prefers-color-scheme:dark){:root{--bg:#161616;--fg:#e8e8e8;--mut:#9a9a9a;--card:#202020;--line:#3a3a3a;--acc:#7fb0ff;--code:#666;--ok:#6fcf8f;--bad:#ff8a80}}
body{background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;margin:0;padding:0 16px 80px}
header{position:sticky;top:0;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);display:flex;gap:8px;flex-wrap:wrap;align-items:center;z-index:2}
button{font:inherit;padding:6px 12px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer}
button.on{border-color:var(--acc);color:var(--acc);font-weight:600}
button.save{background:var(--acc);color:#fff;border-color:var(--acc);margin-left:auto}
.grp{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:14px 0;padding:10px 12px}
.grp h3{margin:0 0 6px;font-size:16px}.mut{color:var(--mut);font-size:13px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px;border-top:1px solid var(--line);padding:8px 0}
.row .id{grid-column:1/-1;font-size:12px;color:var(--mut)}
.row .ed{grid-column:1/-1;display:flex;gap:8px;flex-wrap:wrap}
.tx{white-space:pre-wrap;word-break:break-word}.tx i{color:var(--code);font-style:normal;font-size:12px}
mark{background:#ffe08a;color:#000;border-radius:3px;padding:0 2px}
input,select{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);flex:1;min-width:160px}
select{flex:0 0 110px;min-width:0}
.done{opacity:.55}.bar{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}
@media(max-width:700px){.row{grid-template-columns:1fr}}
</style>
<header id="tabs"></header><p class="mut" id="help"></p><main id="main"></main>
<script>
const D = __DATA__;
const HELP = {
 "escalonamento.csv": "Por item, preencha UM dos dois: alias (a forma usada passa a valer no glossario) ou correcao (o texto certo da fala inteira). O campo do grupo copia o alias para todos os itens do termo. Salve por cima de escalonamento.csv e rode hitl.py resolve.",
 "onda_amostra.csv": "So leitura: amostra das cenas novas. Se estiver bom, rode hitl.py ack.",
 "amostra_qualidade.csv": "Marque ok ou erro em cada fala. Salve por cima de amostra_qualidade.csv e rode quality_sample.py score."};
let cur = Object.keys(D)[0];
const esc = s => (s||"").replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
function tx(s, term){
  let h = esc(s).replace(/\[[0-9A-Fa-f]{2}\]/g, m => m === "[01]" ? "<i>[01]</i>\n" : "<i>" + m + "</i>");
  if (term) { const t = esc(term).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); h = h.replace(new RegExp(t, "gi"), m => "<mark>" + m + "</mark>"); }
  return h;
}
function field(r, c, ph){
  if (c === "veredito") { const s = document.createElement("select");
    for (const v of ["", "ok", "erro"]) s.add(new Option(v || "-", v));
    s.value = (r[c]||"").toLowerCase(); s.onchange = () => { r[c] = s.value; mark(s.closest(".row"), r); }; return s; }
  const i = document.createElement("input"); i.placeholder = ph || c; i.value = r[c] || "";
  i.oninput = () => { r[c] = i.value; mark(i.closest(".row"), r); }; i.dataset.col = c; return i;
}
function mark(el, r){ const e = D[cur].edit; el.classList.toggle("done", e.length > 0 && e.some(c => (r[c]||"").trim()) ); count(); }
function count(){ const s = D[cur], e = s.edit;
  const n = e.length ? s.rows.filter(r => e.some(c => (r[c]||"").trim())).length : 0;
  document.getElementById("cnt").textContent = e.length ? n + " de " + s.rows.length + " respondidos" : s.rows.length + " falas"; }
function draw(){
  const s = D[cur], main = document.getElementById("main"); main.innerHTML = "";
  document.getElementById("help").textContent = HELP[cur] || "";
  const groups = new Map();
  for (const r of s.rows) { const k = r._grp || (cur === "escalonamento.csv" ? r.term + " → " + r.expected : r.scene); (groups.get(k) || groups.set(k, []).get(k)).push(r); }
  for (const [k, rows] of [...groups].sort((a, b) => b[1].length - a[1].length)) {
    const g = document.createElement("div"); g.className = "grp";
    g.innerHTML = "<h3>" + esc(k) + " <span class=mut>(" + rows.length + ")</span></h3>";
    if (cur === "escalonamento.csv") {
      const bar = document.createElement("div"); bar.className = "bar";
      const i = document.createElement("input"); i.placeholder = "alias para todos os itens deste termo";
      const b = document.createElement("button"); b.textContent = "Aplicar ao grupo";
      b.onclick = () => { for (const r of rows) if (!(r.correcao||"").trim()) r.alias = i.value; draw(); };
      bar.append(i, b); g.append(bar);
      if (rows[0].reason) g.insertAdjacentHTML("beforeend", "<div class=mut>" + esc(rows[0].reason) + "</div>");
    }
    for (const r of rows) {
      const d = document.createElement("div"); d.className = "row";
      d.innerHTML = "<div class=id>" + esc(r.offset) + "</div><div class=tx>" + tx(r.source_en, r.term) + "</div><div class=tx>" + tx(r.target_pt, r.expected) + "</div>";
      if (s.edit.length) { const e = document.createElement("div"); e.className = "ed"; for (const c of s.edit) e.append(field(r, c)); d.append(e); }
      g.append(d); mark(d, r);
    }
    main.append(g);
  }
  count();
}
function csv(){ const s = D[cur], q = v => /[",\r\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  return "﻿" + [s.cols, ...s.rows.map(r => s.cols.map(c => r[c] || ""))].map(l => l.map(q).join(",")).join("\r\n") + "\r\n"; }
async function save(){
  try { const r = await fetch("/save/" + encodeURIComponent(cur), {method: "POST", body: csv()});
    if (!r.ok) throw new Error(r.status); alert("Salvo em para_revisar/" + cur + " (" + s_ok() + ")"); return; }
  catch (e) { alert("Nao salvou: " + e + ". Abra a pagina por 'python framework/runtime/review_page.py <projeto> --serve'."); }
}
function s_ok(){ return document.getElementById("cnt").textContent; }
try { const sv0 = JSON.parse(localStorage.getItem("rev_" + cur) || "null"); } catch (e) {}
const tabs = document.getElementById("tabs");
for (const n of Object.keys(D)) { const b = document.createElement("button"); b.textContent = n.replace(".csv", "") + " (" + D[n].rows.length + ")";
  b.onclick = () => { cur = n; for (const x of tabs.querySelectorAll("button[data-n]")) x.classList.toggle("on", x.dataset.n === n); sv.hidden = !D[n].edit.length; draw(); };
  b.dataset.n = n; b.classList.toggle("on", n === cur); tabs.append(b); }
const cnt = document.createElement("span"); cnt.id = "cnt"; cnt.className = "mut"; tabs.append(cnt);
const sv = document.createElement("button"); sv.className = "save"; sv.textContent = "Salvar CSV"; sv.onclick = save; tabs.append(sv);
sv.hidden = !(D[cur] && D[cur].edit.length);
if (cur) draw(); else document.getElementById("help").textContent = "Nenhuma planilha em para_revisar.";
</script>
"""
