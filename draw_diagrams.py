"""Gera 3 diagramas: arquitetura, camadas e governança."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── paleta global ─────────────────────────────────────────────────────────────
COG  = ('#F9D0E4', '#C0397B')   # Cognition — rosa
STA  = ('#FDE6C4', '#C97B1F')   # State     — laranja
EXE  = ('#D6E8F6', '#1F6F9B')   # Execution — azul
VAL  = ('#D9F2D9', '#2E7D32')   # Validation— verde
NEU  = ('#F0F0F0', '#888888')   # neutro
HUM  = ('#FFE4C4', '#C0392B')   # humano    — vermelho-quente
BG   = '#FAFAFA'

# ── helpers compartilhados ────────────────────────────────────────────────────
def bx(ax, x, y, w, h, txt, sub='', fc='#FFF', ec='#444', fs=9.5, sfs=8, bold=False, lw=1.4):
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle='round,pad=0.1',
                                linewidth=lw, edgecolor=ec, facecolor=fc, zorder=3))
    wt = 'bold' if bold else 'normal'
    cy = y+h/2+(0.15 if sub else 0)
    ax.text(x+w/2, cy, txt, ha='center', va='center', fontsize=fs, fontweight=wt, color='#111', zorder=4)
    if sub:
        ax.text(x+w/2, y+h/2-0.22, sub, ha='center', va='center', fontsize=sfs, color='#555', zorder=4)

def ar(ax, x1,y1,x2,y2, col='#555', lw=1.6, rad=None, style='->'):
    kw = dict(arrowstyle=style, color=col, lw=lw)
    if rad is not None:
        kw['connectionstyle'] = f'arc3,rad={rad}'
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=kw, zorder=5)

def banner(ax, x,y,w,h, txt, fc, ec, fs=8.5):
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle='round,pad=0.12',
                                linewidth=2, edgecolor=ec, facecolor=fc+'44', zorder=1))
    ax.text(x+0.15, y+h-0.22, txt, ha='left', va='top', fontsize=fs, fontweight='bold',
            color=ec, zorder=2)

def htag(ax, x, y, txt, fs=7.5):
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold',
            color='#7B0000',
            bbox=dict(boxstyle='round,pad=0.22', facecolor=HUM[0], edgecolor=HUM[1], lw=1.3), zorder=6)

def gtag(ax, x, y, txt, fs=7.5):
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold',
            color='#1A5276',
            bbox=dict(boxstyle='round,pad=0.22', facecolor=EXE[0], edgecolor=EXE[1], lw=1.2), zorder=6)

# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 1 — Arquitetura (organização física do repositório)
# ══════════════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(15, 12))
ax1.set_xlim(0,15); ax1.set_ylim(0,12); ax1.axis('off')
fig1.patch.set_facecolor(BG)

ax1.text(7.5,11.7,'Arquitetura do Repositorio', ha='center', fontsize=15, fontweight='bold', color='#111')
ax1.text(7.5,11.32,'organizacao fisica: framework/ (generico) + projects/ (instancia)', ha='center', fontsize=9, color='#555')

# ── coluna esquerda: framework/ ──────────────────────────────────────────────
banner(ax1, 0.4,0.4, 6.5,10.6, 'framework/   (zero dado de obra)', '#1F6F9B','#1F6F9B', fs=9)

bx(ax1, 0.7,9.2, 5.9,0.85, 'skills/  (00..08)', 'o PROCESSO em prosa — skills do SDD (generico)', fc=EXE[0], ec=EXE[1])
bx(ax1, 0.7,8.05, 5.9,0.85,'runtime/', 'run_scene · context_pack · model · state_index · quality_review', fc=EXE[0], ec=EXE[1])
bx(ax1, 0.7,6.9, 5.9,0.85, 'connectors/', 'extract.py + reinsert.py (skeleton) · hex_binary.md · round-trip', fc=VAL[0], ec=VAL[1])
bx(ax1, 0.7,5.75, 5.9,0.85,'validation/', 'validate.py · naturalness_lint.py · schemas', fc=VAL[0], ec=VAL[1])
bx(ax1, 0.7,4.6, 5.9,0.85, 'media-profiles/', 'games.md  ·  films.md (stub)  ·  series.md (stub)', fc=NEU[0], ec=NEU[1])
bx(ax1, 0.7,3.45, 5.9,0.85,'docs/', 'ARCHITECTURE · GOVERNANCE · CONCEPTS · NAMING · adr/ · ROADMAP', fc=NEU[0], ec=NEU[1])

ax1.text(3.65, 2.9, 'Nenhum dado de obra vive aqui.', ha='center', fontsize=8, color='#444', style='italic')
ax1.text(3.65, 2.6, 'Tudo especifico entra via project.json + artefatos.', ha='center', fontsize=8, color='#444', style='italic')

# ── coluna direita: projects/<obra>/ ─────────────────────────────────────────
banner(ax1, 7.6,0.4, 7.0,10.6, 'projects/<obra>/   (a instancia)', '#C0397B','#C0397B', fs=9)

bx(ax1, 7.9,9.2, 6.4,0.85, 'project.json', 'MANIFESTO: linguas, conector, tokens, budget, batch_size', fc=COG[0], ec=COG[1])
bx(ax1, 7.9,8.05, 6.4,0.85,'profile/', 'voice_profiles · identity_pairs · terminology_seeds · test_suites', fc=COG[0], ec=COG[1])

# artifacts
banner(ax1, 7.9,2.4, 6.4,5.3,'artifacts/', '#888888','#888888', fs=8)
bx(ax1, 8.1,6.25, 5.9,0.75,'glossary.csv  ·  entities.csv  ·  tone_analysis.md', 'KB operacional: fonte de verdade dos termos e vozes', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax1, 8.1,5.2, 5.9,0.75, 'ch_*/  (146 cenas)', 'dialogs.csv · translation_plan · approved_*.csv · back_translation', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax1, 8.1,4.15, 5.9,0.75,'state/', 'translation_memory · voice_cards · decision_index (append-only)', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax1, 8.1,3.1, 5.9,0.75, 'qa_revisao/', 'para_revisar/ (XLSX gerado)  ·  devolvido/ (XLSX do revisor)', fc=HUM[0], ec=HUM[1], fs=8.5)
bx(ax1, 8.1,2.5, 5.9,0.42, 'evidence/  ·  archive/  ·  binarios-fonte', fc=NEU[0], ec=NEU[1], fs=8)

bx(ax1, 7.9,1.4, 6.4,0.75, 'connector/', 'extract.py · reinsert.py · sdat_format.py · build_plan_chapter.py', fc=VAL[0], ec=VAL[1])

bx(ax1, 7.9,0.62, 6.4,0.55,'output/', 'ScriptEvent.sdat (traduzido)  ·  ScriptEvent.sdat.ips (patch)', fc=VAL[0], ec=VAL[1], fs=8.5)

# ── setas framework → projects ───────────────────────────────────────────────
# runtime le project.json + artifacts
ax1.annotate('', xy=(7.9,9.62), xytext=(6.6,9.62),
             arrowprops=dict(arrowstyle='<->', color='#555', lw=1.3), zorder=5)
ax1.text(6.65,9.78,'le/grava', fontsize=7, color='#555')

ax1.annotate('', xy=(7.9,8.47), xytext=(6.6,8.47),
             arrowprops=dict(arrowstyle='->', color='#1F6F9B', lw=1.3), zorder=5)
ax1.text(6.62,8.62,'instancia', fontsize=7, color='#1F6F9B')

# connector bridge
ar(ax1, 6.6,7.32, 7.9,6.62, col='#2E7D32', lw=1.4)
ax1.text(6.5,7.0,'extrai/\nreinsere', fontsize=7, color='#2E7D32', ha='center')

# legenda
items = [(COG,'Cognition (IA)'), (STA,'State (memoria)'), (EXE,'Execution (det.)'),
         (VAL,'Validation (gates)'), (HUM,'Humano'), (NEU,'Suporte/docs')]
for i,(pal,lbl) in enumerate(items):
    lx = 0.6+i*2.45
    ax1.add_patch(FancyBboxPatch((lx,0.12),0.28,0.18,boxstyle='round,pad=0.03',
                                 facecolor=pal[0], edgecolor=pal[1], lw=1.1))
    ax1.text(lx+0.36,0.21,lbl, fontsize=7.5, va='center', color='#333')

plt.tight_layout(pad=0.3)
plt.savefig('diagrama_arquitetura.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('diagrama_arquitetura.png salvo')

# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 2 — Camadas da Arquitetura (4 camadas conceituais)
# ══════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(15, 13))
ax2.set_xlim(0,15); ax2.set_ylim(0,13); ax2.axis('off')
fig2.patch.set_facecolor(BG)

ax2.text(7.5,12.7,'As 4 Camadas da Arquitetura', ha='center', fontsize=15, fontweight='bold', color='#111')
ax2.text(7.5,12.28,'A IA vive SOMENTE na Camada 1 — todo o resto e deterministico', ha='center', fontsize=9, color='#555')

# ── camada 1: COGNITION ───────────────────────────────────────────────────────
banner(ax2, 0.4,9.7, 14.2,2.3, '① COGNITION  —  o que EXIGE IA  (a unica parte estocastica)', COG[0], COG[1], fs=10)
bx(ax2, 0.7,10.85, 4.2,0.85, 'translate', 'IA propoe a traducao\nHaiku (simples) · Sonnet (complexo)', fc=COG[0], ec=COG[1], bold=True)
bx(ax2, 5.2,10.85, 4.2,0.85, 'back_translate', 'IA REVISA (nao julga)\nOpus · SO linhas alto risco', fc=COG[0], ec=COG[1], bold=True)
bx(ax2, 9.7,10.85, 4.6,0.85, 'model.py  (interface unica)', 'unica fronteira com a API\nRuntime agnostico ao modelo', fc=COG[0], ec=COG[1])
bx(ax2, 0.7,9.95, 13.6,0.6, 'Regra de ouro: a IA PROPOE · gates APROVAM · script APLICA · humano tem a PALAVRA FINAL',
   fc='#FFF0F7', ec=COG[1], fs=8.5)

# ── camada 2: STATE ───────────────────────────────────────────────────────────
banner(ax2, 0.4,7.1, 14.2,2.35,'② STATE  —  memoria FORA da janela do modelo', STA[0], STA[1], fs=10)
bx(ax2, 0.7,8.25, 3.2,0.75, 'translation_memory', 'append-only · dedup\nconsistencia entre cenas', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax2, 4.2,8.25, 2.8,0.75, 'glossary.csv', 'fonte de verdade\ndos termos', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax2, 7.3,8.25, 2.8,0.75, 'voice_cards', 'ficha de voz\npor personagem', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax2, 10.4,8.25, 2.4,0.75,'decision_index','decisoes\n(auditavel)', fc=STA[0], ec=STA[1], fs=8.5)
bx(ax2, 13.1,8.25, 1.3,0.75,'spoiler\nledger','frontier', fc=STA[0], ec=STA[1], fs=8)
bx(ax2, 0.7,7.3, 13.6,0.65, 'Vive em artifacts/state/  ·  versionado  ·  sem banco, sem embeddings, sem 2o servico pago',
   fc='#FFF8EE', ec=STA[1], fs=8.5)

# ── camada 3: EXECUTION ───────────────────────────────────────────────────────
banner(ax2, 0.4,4.45, 14.2,2.4,'③ EXECUTION  —  orquestracao deterministica', EXE[0], EXE[1], fs=10)
bx(ax2, 0.7,5.65, 3.2,0.75, 'context_pack', 'monta pacote O(cena)\nglosario + vozes + linhas', fc=EXE[0], ec=EXE[1], fs=8.5)
bx(ax2, 4.2,5.65, 2.8,0.75, 'run_scene.py', 'cena = job\nstateless', fc=EXE[0], ec=EXE[1], fs=8.5)
bx(ax2, 7.3,5.65, 3.0,0.75, 'run_chapter.py', 'orquestra\npor capitulo', fc=EXE[0], ec=EXE[1], fs=8.5)
bx(ax2, 10.6,5.65, 3.8,0.75,'connector\n(extract + reinsert)', 'deterministico\nbinario <-> corpus', fc=EXE[0], ec=EXE[1], fs=8.5)
bx(ax2, 0.7,4.65, 13.6,0.7, 'Cada cena = funcao pura: recebe context_pack, devolve traducao, nao guarda historico  ·  checkpoint/resume',
   fc='#EAF3FB', ec=EXE[1], fs=8.5)

# ── camada 4: VALIDATION ─────────────────────────────────────────────────────
banner(ax2, 0.4,1.8, 14.2,2.4,'④ VALIDATION  —  gates que BLOQUEIAM', VAL[0], VAL[1], fs=10)
bx(ax2, 0.7,3.0, 2.8,0.75, 'round-trip', 'extract -> reinsert\nbyte-identico', fc=VAL[0], ec=VAL[1], fs=8.5)
bx(ax2, 3.8,3.0, 2.8,0.75, 'KB gate', 'entidade sem fonte\nBLOQUEIA', fc=VAL[0], ec=VAL[1], fs=8.5)
bx(ax2, 6.9,3.0, 2.8,0.75, 'spoiler gate','nome antes do\nreveal BLOQUEIA', fc=VAL[0], ec=VAL[1], fs=8.5)
bx(ax2, 10.0,3.0, 2.3,0.75,'naturalness\nlinter','smells\nde pt-BR', fc=VAL[0], ec=VAL[1], fs=8.5)
bx(ax2, 12.6,3.0, 1.8,0.75,'largura\nbalao','segmento\n>62 chars', fc=VAL[0], ec=VAL[1], fs=8.5)
bx(ax2, 0.7,2.0, 13.6,0.7, 'Gates sao os unicos atores que BLOQUEIAM o avanco  ·  Reproducivel: mesma entrada -> mesma decisao  ·  $0 de IA',
   fc='#EAF9EA', ec=VAL[1], fs=8.5)

# ── setas entre camadas ───────────────────────────────────────────────────────
for y_top, y_bot, col in [(9.7,9.45,COG[1]),(7.1,6.85,STA[1]),(4.45,4.2,EXE[1])]:
    ar(ax2, 7.5,y_top, 7.5,y_bot, col=col, lw=1.8)

# seta de reprovacao: VAL -> EXE
ax2.annotate('', xy=(14.35,5.85), xytext=(14.35,3.75),
             arrowprops=dict(arrowstyle='->', color=VAL[1], lw=1.6), zorder=5)
ax2.text(14.45,4.8,'reprova\nnao avanca', fontsize=7.5, color=VAL[1], ha='left', va='center')

# ── fluxo de uma cena (parte de baixo) ───────────────────────────────────────
ax2.text(7.5,1.58,'Fluxo de uma cena (as duas unicas chamadas de IA):', ha='center', fontsize=8.5, fontweight='bold', color='#333')
steps = [
    (0.5, 'context_pack\n(monta contexto)', EXE),
    (2.9, 'translate\n(IA · Sonnet)', COG),
    (5.3, 'build_plan\n(monta approved)', EXE),
    (7.7, 'back_translate\n(IA · Opus  so alto risco)', COG),
    (10.6,'verify\n(round-trip + gates)', VAL),
    (13.1,'checkpoint + TM\n(grava estado)', STA),
]
for i,(x,t,pal) in enumerate(steps):
    bx(ax2, x,0.2, 2.2,0.9, t, fc=pal[0], ec=pal[1], fs=7.8)
    if i < len(steps)-1:
        ar(ax2, x+2.2,0.65, steps[i+1][0],0.65, col='#555', lw=1.3)

plt.tight_layout(pad=0.3)
plt.savefig('diagrama_camadas.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('diagrama_camadas.png salvo')

# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA 3 — Governança
# ══════════════════════════════════════════════════════════════════════════════
fig3, ax3 = plt.subplots(figsize=(15, 14))
ax3.set_xlim(0,15); ax3.set_ylim(0,14); ax3.axis('off')
fig3.patch.set_facecolor(BG)

ax3.text(7.5,13.7,'Governanca', ha='center', fontsize=15, fontweight='bold', color='#111')
ax3.text(7.5,13.28,'quem propoe · quem aprova · quem aplica · quem julga', ha='center', fontsize=9, color='#555')

# ── cadeia central ─────────────────────────────────────────────────────────────
ax3.text(7.5,12.85,'A cadeia de aprovacao (inviolavel):', ha='center', fontsize=10, fontweight='bold', color='#333')

chain = [
    (0.5,  'IA PROPOE\n(translate)', COG, 'base_translation\nno plano'),
    (3.7,  'GATES\nAPROVAM\n(deterministicos)', VAL, 'round-trip · KB · spoiler\nlargura · naturalidade'),
    (7.5,  'HUMANO\nRATIFICA\n(palavra final)', HUM, 'KB + revisao\ntexto + tela'),
    (11.3, 'SCRIPT\nAPLICA\n(deterministico)', EXE, 'approved_*.csv\n-> binario'),
    (13.5, 'DADO\nCANONICO', STA, 'versionado\nauditavel'),
]
for i,(x,t,pal,sub) in enumerate(chain):
    bx(ax3, x,11.1, 2.1,1.45, t, sub=sub, fc=pal[0], ec=pal[1], bold=True, fs=9.5, sfs=7.5, lw=2)
    if i < len(chain)-1:
        nx = chain[i+1][0]
        ar(ax3, x+2.1,11.82, nx,11.82, col='#333', lw=2.0)

ax3.text(7.5,10.82,'Nenhuma traducao entra no dado canonico sem provar que passou por todos os gates.', ha='center', fontsize=8.5, color='#444', style='italic')

# ── 3 papeis humanos ──────────────────────────────────────────────────────────
banner(ax3, 0.4,7.8, 14.2,2.75,'Papeis Humanos  (fronteiras explicitas)', HUM[0], HUM[1], fs=9)

bx(ax3, 0.7,9.0, 4.2,1.2, 'HUMANO-RATIFICADOR', 'Confirma entidade/genero COM FONTE\n-> kb_ratified.csv\nNao traduz linha a linha', fc=HUM[0], ec=HUM[1], bold=True, fs=9, sfs=8)
bx(ax3, 5.2,9.0, 4.2,1.2, 'HUMANO-REVISOR', 'Le o XLSX (review_all.xlsx)\nEscreve CORRIGIR + texto certo / nota\nNao mexe no binario', fc=HUM[0], ec=HUM[1], bold=True, fs=9, sfs=8)
bx(ax3, 9.7,9.0, 4.8,1.2, 'HUMANO-TESTER\n(in-game)', 'Joga e reporta: print + trecho do texto visto\n-> relato_tester.csv (localizador det., $0)\nNao usa IA/OCR', fc=HUM[0], ec=HUM[1], bold=True, fs=9, sfs=8)

bx(ax3, 0.7,8.0, 13.6,0.7,'A IA REVISA (back-translation APONTA) · mas quem JULGA e o gate (objetivo) ou o HUMANO (sentido e gosto)',
   fc='#FFF8EE', ec=HUM[1], fs=8.5)

# ── 4 diretrizes da carta ─────────────────────────────────────────────────────
banner(ax3, 0.4,3.6, 14.2,4.0,'Carta de Governanca  —  As 4 Diretrizes (transversal Passos 05–08)', '#8E44AD','#8E44AD', fs=9)

bx(ax3, 0.7,5.95, 3.3,1.3, '① PERSONAGEM\n(voz)', 'Respeitar perfil de voz do falante\nIdentidade dupla: nunca revelar\nantes do reveal_timing\nVoz consistente: mesma pessoa', fc='#F5EEF8', ec='#8E44AD', fs=8.5, sfs=7.8)
bx(ax3, 4.3,5.95, 3.3,1.3, '② MUNDO\n(lore)', 'Termos do glossary.csv\nna forma exata\nHonorifico e formalidade\nconforme relacao no mundo\nSPOILER: nunca antes do reveal', fc='#F5EEF8', ec='#8E44AD', fs=8.5, sfs=7.8)
bx(ax3, 8.0,5.95, 3.1,1.3, '③ SITUACAO\n(cena/emocao)', 'Traduzir pela intencao/emocao\nnao pela letra\nInterjeicoes: localizar\n(nunca copiar do source)\npt-BR moderno do jogador de hoje', fc='#F5EEF8', ec='#8E44AD', fs=8.5, sfs=7.8)
bx(ax3, 11.4,5.95, 3.2,1.3, '④ PROCESSO\n(qualidade)', 'IA propoe no plano\nHumano aprova\nScript aplica\nDecisoes nao-obvias\nvao pro decision_log', fc='#F5EEF8', ec='#8E44AD', fs=8.5, sfs=7.8)

# checklist resumido
bx(ax3, 0.7,4.1, 13.6,1.6,
   'Checklist por linha (executar antes de aceitar)',
   'Voz bate com o perfil do falante?  ·  Nada revelado antes do reveal_timing?  ·  '
   'Termos do glossario na forma certa?  ·  Traduzido pela emocao/intencao?  ·\n'
   'Naturalidade: um nativo le NESTA situacao e entende facil?  ·  '
   'pt-BR moderno (ex.: "Meu nome e", nao "Eu sou")?  ·  Cabe/translitera no conector?  ·  '
   'Se risco >= high: passou por back-translation?',
   fc='#F5EEF8', ec='#8E44AD', fs=9, sfs=8)

# ── gates deterministicos ─────────────────────────────────────────────────────
banner(ax3, 0.4,0.8, 14.2,2.55,'Gates Deterministicos  (bloqueiam — $0 de IA)', VAL[0], VAL[1], fs=9)

gates = [
    ('round-trip', 'extract -> reinsert\nbyte-identico\n(oraculo de integridade)'),
    ('KB gate', 'entidade nova\nsem fonte declarada\nBLOQUEIA'),
    ('spoiler gate', 'nome/revelacao\nantes do reveal\nBLOQUEIA'),
    ('naturalness\nlinter', 'smells de pt-BR\n(identico-fonte, pt-PT,\ntamanho outlier)'),
    ('largura de\nbalao', 'segmento > 62 chars\nestoura in-game\n(ESTOUROU)'),
    ('back-translation', 'verdict "revise"\n(APONTA — nao\nbloqueia sozinho)'),
]
for i,(t,s) in enumerate(gates):
    bx(ax3, 0.5+i*2.42, 1.05, 2.2,1.1, t, s, fc=VAL[0], ec=VAL[1], fs=8.5, sfs=7.5)

plt.tight_layout(pad=0.3)
plt.savefig('diagrama_governanca.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('diagrama_governanca.png salvo')
