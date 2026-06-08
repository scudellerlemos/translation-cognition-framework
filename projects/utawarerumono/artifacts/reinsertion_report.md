# Reinsertion Report — Utawarerumono (POC 20 linhas)

- Round-trip self-test: OK
- Saída: output/ScriptEvent.sdat (mesmo nome/extensão do input)
- Patch: output/ScriptEvent.sdat.ips
- Charset: TRANSLITERAÇÃO na gravação (fonte sem diacríticos — evidência char1/char2.png)
- Distribuição por tier: REPOINT_cont=1, REPOINT_head=7, T1_in_place=12
- Overflows não resolvidos (T4): 0

## Repoints (head -> novo offset)

| head | novo offset | ponteiros reescritos | membros do run |
|---|---|---|---|
| 0x3442 | 0x31f570 | 0x11572e | 0x3442 |
| 0x3450 | 0x31f581 | 0x23c302, 0x2927ce | 0x3450 |
| 0x3479 | 0x31f5b0 | 0xac30d | 0x3479 |
| 0x3494 | 0x31f5cc | 0x2303ba, 0x319a5b | 0x3494 |
| 0x34d4 | 0x31f5ee | 0x23c352 | 0x34d4 |
| 0x35ad | 0x31f60d | 0x2e06aa | 0x35ad, 0x35bf |
| 0x35ed | 0x31f652 | 0x13a610, 0x211edb | 0x35ed |

## Strings

| offset | tier | bytes | budget | texto |
|---|---|---|---|---|
| 0x3398 | T1_in_place | 13 | 13 | Ngh... ghh... |
| 0x33a6 | T1_in_place | 7 | 7 | Nn...\n |
| 0x33ae | T1_in_place | 16 | 16 | Ta... quente...? |
| 0x33bf | T1_in_place | 3 | 3 | Nh? |
| 0x33c3 | T1_in_place | 9 | 9 | Q-Quem... |
| 0x33cd | T1_in_place | 15 | 21 | ...me chama...? |
| 0x33e3 | T1_in_place | 20 | 21 | Pera... eu ainda...! |
| 0x33f9 | T1_in_place | 71 | 72 | INICIANDO PROCESSO DE DESPERTAR. SISTEMAS... REINICIANDO EM 5 SEGUNDOS. |
| 0x3442 | REPOINT_head | 16 | 13 | ERRO DE SISTEMA. |
| 0x3450 | REPOINT_head | 46 | 40 | PROBLEMA DETECTADO NO PROCESSO DE DESPERTAR.\n |
| 0x3479 | REPOINT_head | 27 | 26 | SUJEITO GRAVEMENTE AFETADO. |
| 0x3494 | REPOINT_head | 33 | 28 | COMANDO DE ABORTAR: CANCELADO. \n |
| 0x34b1 | T1_in_place | 33 | 34 | IMPOSSIVEL ENCERRAR O PROCESSO.\n |
| 0x34d4 | REPOINT_head | 30 | 21 | INICIANDO CONTAGEM REGRESSIVA. |
| 0x34ea | T1_in_place | 36 | 36 | 5, {W75}4, {W75}3, {W80}2, {W80}1... |
| 0x350f | T1_in_place | 134 | 137 | T{W10}E{W10}N{W10}H{W10}A{W10} {W10}U{W10}M{W10} {W10}B{W10}O{W10}M{W10} {W10}D{W10}E{W10}S{W10}P{W10}E{W10}R{W10}T{W10}A{W10}R{W10}-- |
| 0x359d | T1_in_place | 14 | 15 | On... Onde...? |
| 0x35ad | REPOINT_head | 17 | 17 | Onde... estou...? |
| 0x35bf | REPOINT_cont | 50 | 45 | Acima de mim... uma especie de... teto de pano...? |
| 0x35ed | REPOINT_head | 53 | 49 | Quase nenhuma luz...... Ou so esta escuro la fora...? |