import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(14, 22))
ax.set_xlim(0, 14)
ax.set_ylim(0, 22)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

# ── helpers ──────────────────────────────────────────────────────────────────
def box(ax, x, y, w, h, label, sublabel='', color='#FFFFFF', border='#444444',
        fontsize=10, subfontsize=8.5, bold=False):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.12", linewidth=1.5,
                          edgecolor=border, facecolor=color, zorder=3)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    cy = y + h/2 + (0.18 if sublabel else 0)
    ax.text(x + w/2, cy, label, ha='center', va='center',
            fontsize=fontsize, fontweight=weight, color='#1A1A1A', zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.25, sublabel, ha='center', va='center',
                fontsize=subfontsize, color='#555555', zorder=4)

def arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw), zorder=5)

def curved_arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.4, rad=0.3):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'), zorder=5)

def phase_bg(ax, x, y, w, h, label, color):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.15", linewidth=2,
                          edgecolor=color, facecolor=color + '22', zorder=1)
    ax.add_patch(rect)
    ax.text(x + 0.18, y + h - 0.28, label, ha='left', va='top',
            fontsize=8.5, fontweight='bold', color=color, zorder=2)

def human_tag(ax, x, y, label='DECISAO HUMANA'):
    ax.text(x, y, label, ha='center', va='center',
            fontsize=7.5, color='#8B0000', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFE4E4',
                      edgecolor='#C0392B', linewidth=1.3), zorder=6)

def gate_tag(ax, x, y, label):
    ax.text(x, y, label, ha='center', va='center',
            fontsize=7.5, color='#1A5276', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#D6EAF8',
                      edgecolor='#2980B9', linewidth=1.2), zorder=6)

# ── título ────────────────────────────────────────────────────────────────────
ax.text(7, 21.55, 'Fluxo de Traducao — Utawarerumono (Mask of Deception)',
        ha='center', va='top', fontsize=14, fontweight='bold', color='#1A1A1A')
ax.text(7, 21.1, 'visao de alto nivel  ·  do binario ao patch',
        ha='center', va='top', fontsize=9, color='#666666')

# ── binário fonte ─────────────────────────────────────────────────────────────
box(ax, 4.2, 20.25, 5.6, 0.6, 'BINARIO-FONTE  (ScriptEvent.sdat)',
    color='#D5D8DC', border='#717D7E', fontsize=10, bold=True)
arrow(ax, 7, 20.25, 7, 19.75)

# ─────────────────────────────────────────────────────────────────────────────
# FASE 1 — Preparação
# ─────────────────────────────────────────────────────────────────────────────
phase_bg(ax, 0.4, 15.35, 13.2, 4.25, 'FASE 1  —  Preparacao', '#2980B9')

# linha 1: 00 / 01 / 02
box(ax, 0.7, 18.9, 3.9, 0.65, '00  Extracao',
    'extract.py  ->  dialogs.csv + byte_budget',
    color='#D6EAF8', border='#2980B9')
box(ax, 4.9, 18.9, 3.9, 0.65, '01  Discovery',
    'entidades, tom, aliases, spoilers',
    color='#D6EAF8', border='#2980B9')
box(ax, 9.1, 18.9, 3.9, 0.65, '02  Entity Resolution',
    'classificar e unificar entidades',
    color='#D6EAF8', border='#2980B9')
arrow(ax, 4.6,  19.22, 4.9,  19.22)
arrow(ax, 8.8,  19.22, 9.1,  19.22)

# linha 2: 03 / 04
box(ax, 0.7, 17.65, 5.8, 0.75, '03  Knowledge Building',
    'research_log.md  ·  universe_knowledge_base.md',
    color='#D6EAF8', border='#2980B9')
box(ax, 7.1, 17.65, 5.8, 0.75, '04  Glossario + Decision Log',
    'fonte de verdade operacional dos termos',
    color='#D6EAF8', border='#2980B9')

# 02 desce pra 03
arrow(ax, 11.05, 18.9, 3.6, 18.4)
# 03 -> 04 (com tag humano no meio)
arrow(ax, 6.5, 18.02, 7.1, 18.02)
human_tag(ax, 6.85, 18.38, label='DECISAO HUMANA\n(KB reconciliada)')

# gate
box(ax, 0.7, 15.6, 12.6, 0.65,
    'GATE:  round-trip byte-identico (Extracao)  +  KB reconciliada por fonte confiaevel (Passo 03)',
    color='#EBF5FB', border='#7FB3D3', fontsize=8.5)
arrow(ax, 7, 15.6, 7, 15.35)

# ─────────────────────────────────────────────────────────────────────────────
# FASE 2 — Planejamento
# ─────────────────────────────────────────────────────────────────────────────
phase_bg(ax, 0.4, 13.35, 13.2, 1.8, 'FASE 2  —  Planejamento', '#8E44AD')

box(ax, 0.7, 13.6, 5.8, 0.85, '05  Translation Planning',
    'translation_plan.json  ·  risk_level  ·  byte_budget por linha',
    color='#E8DAEF', border='#8E44AD')
box(ax, 7.1, 13.6, 5.8, 0.85, '05b  Synthetic Test Corpus',
    'suites de teste para pontos criticos de identidade',
    color='#E8DAEF', border='#8E44AD')
arrow(ax, 6.5, 14.02, 7.1, 14.02)
arrow(ax, 7, 13.6, 7, 13.35)

# ─────────────────────────────────────────────────────────────────────────────
# FASE 3 — Tradução (loop por cena)
# ─────────────────────────────────────────────────────────────────────────────
phase_bg(ax, 0.4, 9.55, 13.2, 3.6,
         'FASE 3  —  Traducao por cena  (loop  ·  capitulo a capitulo)', '#27AE60')

box(ax, 0.7, 11.85, 3.9, 0.85, '06  Traducao',
    'IA em lotes  ·  auto-revisao de voz\n-> approved_*.csv',
    color='#D5F5E3', border='#27AE60')
box(ax, 5.05, 11.85, 3.9, 0.85, '06b  Micro QA',
    'back-translation  ·  voz\ntokens  ·  entidades',
    color='#D5F5E3', border='#27AE60')
box(ax, 9.4, 11.85, 3.9, 0.85, '06c  Ciclo de Correcao',
    'cirurgico  ·  so IDs\ndo escopo reprovado',
    color='#D5F5E3', border='#27AE60')

arrow(ax, 4.6, 12.27, 5.05, 12.27)        # 06 -> 06b

# 06b -> 06c (reprovado, sobe)
curved_arrow(ax, 8.95, 12.65, 9.4, 12.65, color='#C0392B', rad=-0.3)
ax.text(8.5, 13.02, 'reprovado', fontsize=7.5, color='#C0392B', fontstyle='italic')

# 06c -> 06b (re-valida, desce)
curved_arrow(ax, 9.4, 11.85, 8.95, 11.85, color='#27AE60', rad=0.3)
ax.text(9.1, 11.5, 're-valida', fontsize=7.5, color='#1A8048', fontstyle='italic')

# 06b -> proximo lote -> 06 (aprovado, curva por baixo)
curved_arrow(ax, 5.05, 11.85, 4.6, 11.85, color='#27AE60', rad=0.35)
ax.text(3.3, 11.5, 'proximo lote', fontsize=7.5, color='#1A8048', fontstyle='italic')

# orquestração
box(ax, 1.5, 9.82, 11, 0.75,
    'run_chapter.py   ·   run_scene.py   ·   verify_chapter.py',
    'scripts de orquestracao — executam passos 06 / 06b / 06c por cena',
    color='#FDFEFE', border='#A9DFBF', fontsize=9)
arrow(ax, 7, 9.82, 7, 9.55)

# ─────────────────────────────────────────────────────────────────────────────
# FASE 4 — QA Final + Revisão Humana
# ─────────────────────────────────────────────────────────────────────────────
phase_bg(ax, 0.4, 6.1, 13.2, 3.25, 'FASE 4  —  QA Final + Revisao Humana', '#E67E22')

box(ax, 0.7, 8.05, 3.4, 0.85, '07  QA Final',
    'qa_report.md\nfix_suggestions.json',
    color='#FDEBD0', border='#E67E22')
box(ax, 4.4, 8.05, 3.4, 0.85, 'quality_review.py\nexport',
    'gera review_all.xlsx\npara o revisor humano',
    color='#FDEBD0', border='#E67E22')
box(ax, 8.1, 8.05, 5.2, 0.85, 'REVISOR le o XLSX',
    'escreve CORRIGIR + texto certo  ou  nota de instrucao para a IA',
    color='#FFE4C4', border='#C0392B', bold=True)

human_tag(ax, 10.7, 9.15, label='DECISAO HUMANA')

box(ax, 0.7, 6.55, 6.5, 0.85, 'quality_review.py apply',
    'verbatim ($0)  ou  IA cirurgica por linha  ·  re-roda QA se houve correcao',
    color='#FDEBD0', border='#E67E22')

arrow(ax, 4.1, 8.47, 4.4, 8.47)
arrow(ax, 7.8, 8.47, 8.1, 8.47)

# revisor -> apply (desce pela direita)
arrow(ax, 10.7, 8.05, 10.7, 7.42)
arrow(ax, 10.7, 7.42, 7.2, 7.42)
ax.annotate('', xy=(7.2, 7.42), xytext=(10.7, 7.42),
            arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.5), zorder=5)

# apply -> re-QA loop (se corrigiu)
curved_arrow(ax, 3.95, 6.55, 2.4, 6.55, color='#E67E22', rad=0.5)
ax.text(0.55, 6.78, 're-QA\nse corrigiu', fontsize=7, color='#784212', fontstyle='italic')

arrow(ax, 7, 6.55, 7, 6.1)

# gate final
box(ax, 0.7, 5.82, 12.6, 0.55,
    'GATE:  0 issues criticos  ·  fix_suggestions todos aplicados  ·  QA aprovado',
    color='#EBF5FB', border='#F0B27A', fontsize=8.5)
arrow(ax, 7, 5.82, 7, 5.55)

# ─────────────────────────────────────────────────────────────────────────────
# FASE 5 — Reinserção
# ─────────────────────────────────────────────────────────────────────────────
phase_bg(ax, 0.4, 2.85, 13.2, 2.55, 'FASE 5  —  Reinsercao', '#C0392B')

box(ax, 0.7, 4.45, 12.6, 0.75, '08  reinsert_game.py',
    '146 cenas  ·  45 141 linhas  ·  cascata T1-T3 deterministica  ·  '
    'T4 LLM so no residuo  ·  round-trip + read-back verdes',
    color='#FADBD8', border='#C0392B')

box(ax, 0.7, 3.1, 5.6, 0.9, 'output/ScriptEvent.sdat',
    'binario traduzido  ·  pronto para o jogo',
    color='#FADBD8', border='#922B21', bold=True)
box(ax, 7.7, 3.1, 5.6, 0.9, 'output/ScriptEvent.sdat.ips',
    'patch IPS  ·  aplicar sobre o original da Steam',
    color='#FADBD8', border='#922B21', bold=True)

arrow(ax, 4.75, 4.45, 3.5, 4.0)
arrow(ax, 9.25, 4.45, 10.5, 4.0)

# ── legenda ───────────────────────────────────────────────────────────────────
leg_items = [
    ('#D6EAF8', '#2980B9', 'Preparacao'),
    ('#E8DAEF', '#8E44AD', 'Planejamento'),
    ('#D5F5E3', '#27AE60', 'Traducao (loop)'),
    ('#FDEBD0', '#E67E22', 'QA + Revisao'),
    ('#FADBD8', '#C0392B', 'Reinsercao'),
    ('#FFE4C4', '#C0392B', 'Intervencao humana'),
]
ax.text(0.7, 2.55, 'Legenda:', fontsize=8, fontweight='bold', color='#333')
for i, (fc, ec, label) in enumerate(leg_items):
    lx = 0.7 + i * 2.2
    r = FancyBboxPatch((lx, 2.1), 0.32, 0.22,
                       boxstyle="round,pad=0.04", facecolor=fc, edgecolor=ec, linewidth=1.2)
    ax.add_patch(r)
    ax.text(lx + 0.42, 2.21, label, fontsize=7.5, va='center', color='#333')

plt.tight_layout(pad=0.3)
plt.savefig('flow_diagram.png', dpi=160, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print('salvo: flow_diagram.png')
