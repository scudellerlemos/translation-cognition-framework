# Reinsertion Report — Utawarerumono (POC 20 linhas)

- Round-trip self-test: OK
- Saída: output/ScriptEvent.sdat (mesma extensão do input)
- Aplicadas in_place (cabem): 12/20
- Resíduo T4 (estouram byte_budget): 8/20 — exigem repoint ou abreviação

| offset | tier | pt_bytes | budget | texto |
|---|---|---|---|---|
| 0x3398 | T1_in_place | 13 | 13 | Ngh... ghh... |
| 0x33a6 | T1_in_place | 7 | 7 | Nn...\n |
| 0x33ae | T4_residuo | 17 | 16 | Tá... quente...? |
| 0x33bf | T1_in_place | 3 | 3 | Nh? |
| 0x33c3 | T1_in_place | 9 | 9 | Q-Quem... |
| 0x33cd | T1_in_place | 15 | 21 | ...me chama...? |
| 0x33e3 | T1_in_place | 20 | 21 | Pera... eu ainda...! |
| 0x33f9 | T1_in_place | 71 | 72 | INICIANDO PROCESSO DE DESPERTAR. SISTEMAS... REINICIANDO EM 5 SEGUNDOS. |
| 0x3442 | T4_residuo | 16 | 13 | ERRO DE SISTEMA. |
| 0x3450 | T4_residuo | 46 | 40 | PROBLEMA DETECTADO NO PROCESSO DE DESPERTAR.\n |
| 0x3479 | T4_residuo | 27 | 26 | SUJEITO GRAVEMENTE AFETADO. |
| 0x3494 | T4_residuo | 33 | 28 | COMANDO DE ABORTAR: CANCELADO. \n |
| 0x34b1 | T1_in_place | 34 | 34 | IMPOSSÍVEL ENCERRAR O PROCESSO.\n |
| 0x34d4 | T4_residuo | 30 | 21 | INICIANDO CONTAGEM REGRESSIVA. |
| 0x34ea | T1_in_place | 36 | 36 | 5, {W75}4, {W75}3, {W80}2, {W80}1... |
| 0x350f | T1_in_place | 134 | 137 | T{W10}E{W10}N{W10}H{W10}A{W10} {W10}U{W10}M{W10} {W10}B{W10}O{W10}M{W10} {W10}D{W10}E{W10}S{W10}P{W10}E{W10}R{W10}T{W10}A{W10}R{W10}-- |
| 0x359d | T1_in_place | 14 | 15 | On... Onde...? |
| 0x35ad | T1_in_place | 17 | 17 | Onde... estou...? |
| 0x35bf | T4_residuo | 51 | 45 | Acima de mim... uma espécie de... teto de pano...? |
| 0x35ed | T4_residuo | 56 | 49 | Quase nenhuma luz...... Ou só está escuro lá fora...? |