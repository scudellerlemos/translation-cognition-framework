# CLAUDE.md — translation-cognition-framework

## Ferramentas de reverse engineering (uso automático, sem pedir permissão)

- Kaitai Struct (Web IDE ide.kaitai.io ou compiler local) + ImHex: ao iniciar Fase 0 de descoberta de conector novo (formato binário desconhecido), antes de escrever extract.py à mão.
- Hypothesis: ao escrever/revisar test_roundtrip_synthetic.py de qualquer conector.
- vbindiff: sempre que um teste de round-trip falhar, antes de debugar no código.
- binwalk: primeiro passo ao receber arquivo binário de jogo desconhecido.
- GARbro: ao identificar jogo novo de engine de visual novel conhecida.
- FModel: se o jogo novo for Unreal Engine (.pak/.uasset).
- UndertaleModTool: se o jogo novo for GameMaker (data.win).
- UABEA: companion do UnityPy quando ele não parsear uma versão nova do Unity.

Nunca usar fora do contexto de bring-up/debug de conector — apoio à fase de descoberta, não dependência de pipeline em produção.
