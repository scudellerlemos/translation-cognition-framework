# Reinsertion Report — Utawarerumono (POC 20 linhas)

- Round-trip self-test: OK
- Saída: output/ScriptEvent.sdat (mesmo nome/extensão do input)
- Patch: output/ScriptEvent.sdat.ips
- Charset: TRANSLITERAÇÃO na gravação (fonte sem diacríticos — evidência char1/char2.png)
- Distribuição por tier: REPOINT_cont=5, REPOINT_head=425, T1_in_place=595
- Overflows não resolvidos (T4): 0

## Repoints (head -> novo offset)

| head | novo offset | ponteiros reescritos | membros do run |
|---|---|---|---|
| 0x33ae | 0x31f570 | 0x261d | 0x33ae |
| 0x33e3 | 0x31f583 | 0x27b7 | 0x33e3 |
| 0x33f9 | 0x31f59a | 0x27cf | 0x33f9 |
| 0x3419 | 0x31f5bb | 0x27ed | 0x3419 |
| 0x3442 | 0x31f5ea | 0x280b | 0x3442 |
| 0x3450 | 0x31f5fb | 0x2829 | 0x3450 |
| 0x3479 | 0x31f62a | 0x2831 | 0x3479 |
| 0x3494 | 0x31f646 | 0x284f | 0x3494 |
| 0x34d4 | 0x31f668 | 0x285f | 0x34d4 |
| 0x35bf | 0x31f687 | 0x2a43 | 0x35bf |
| 0x35ed | 0x31f6ba | 0x2a5b | 0x35ed |
| 0x366a | 0x31f6f0 | 0x2ac3 | 0x366a |
| 0x3697 | 0x31f702 | 0x2ba3 | 0x3697, 0x36a0 |
| 0x36fa | 0x31f713 | 0x2bdb | 0x36fa |
| 0x37a2 | 0x31f743 | 0x2c5b | 0x37a2 |
| 0x37d3 | 0x31f775 | 0x2c63 | 0x37d3 |
| 0x37f8 | 0x31f78f | 0x2d17 | 0x37f8 |
| 0x38a3 | 0x31f7ab | 0x2e09 | 0x38a3, 0x38b1 |
| 0x38b7 | 0x31f7bf | 0x2eae | 0x38b7 |
| 0x398f | 0x31f7ee | 0x2f53 | 0x398f |
| 0x39bc | 0x31f81e | 0x2fca | 0x39bc |
| 0x39f0 | 0x31f855 | 0x2fd2 | 0x39f0 |
| 0x3a29 | 0x31f869 | 0x3061 | 0x3a29 |
| 0x3a80 | 0x31f88f | 0x3081 | 0x3a80, 0x3a9f |
| 0x3af3 | 0x31f8b2 | 0x3118 | 0x3af3 |
| 0x3b69 | 0x31f8d1 | 0x31d7 | 0x3b69 |
| 0x3ba7 | 0x31f8df | 0x31f7 | 0x3ba7 |
| 0x3bf0 | 0x31f8f6 | 0x3301 | 0x3bf0 |
| 0x3c01 | 0x31f909 | 0x3319 | 0x3c01 |
| 0x7da5 | 0x31f91f | 0x3e20 | 0x7da5 |
| 0x7dd5 | 0x31f93c | 0x404a | 0x7dd5 |
| 0x7df6 | 0x31f952 | 0x40d1 | 0x7df6 |
| 0x7e29 | 0x31f975 | 0x4129 | 0x7e29 |
| 0x7edc | 0x31f9a7 | 0x4162 | 0x7edc |
| 0x7f20 | 0x31f9c7 | 0x4192 | 0x7f20 |
| 0x7f2f | 0x31f9de | 0x41a3 | 0x7f2f |
| 0x7f80 | 0x31fa07 | 0x41dd | 0x7f80 |
| 0x7f9e | 0x31fa24 | 0x4275 | 0x7f9e |
| 0x7fd1 | 0x31fa58 | 0x427d | 0x7fd1 |
| 0x7ffa | 0x31fa85 | 0x42a7 | 0x7ffa |
| 0x800b | 0x31fa91 | 0x432d | 0x800b |
| 0x8021 | 0x31faad | 0x435c | 0x8021 |
| 0x803a | 0x31fac8 | 0x4386 | 0x803a |
| 0x80ce | 0x31fae8 | 0x4401 | 0x80ce |
| 0x811f | 0x31fafc | 0x44e7 | 0x811f |
| 0x815d | 0x31fb2d | 0x459c | 0x815d |
| 0x81ca | 0x31fb5e | 0x45db | 0x81ca |
| 0x822b | 0x31fb91 | 0x4644 | 0x822b |
| 0x8237 | 0x31fba0 | 0x4655 | 0x8237 |
| 0x830b | 0x31fbd0 | 0x46f5 | 0x830b |
| 0x8386 | 0x31fc0a | 0x471d | 0x8386 |
| 0x83ac | 0x31fc35 | 0x4735 | 0x83ac |
| 0x83dd | 0x31fc67 | 0x473d | 0x83dd |
| 0x83ea | 0x31fc76 | 0x474e | 0x83ea |
| 0x86a6 | 0x31fca8 | 0x4aeb | 0x86a6 |
| 0x8762 | 0x31fcbe | 0x4b47 | 0x8762 |
| 0x877a | 0x31fcd8 | 0x4bad | 0x877a |
| 0x8799 | 0x31fce2 | 0x4be6 | 0x8799 |
| 0x87c3 | 0x31fd11 | 0x4c5b | 0x87c3 |
| 0x87dd | 0x31fd32 | 0x4c99 | 0x87dd |
| 0x885a | 0x31fd5d | 0x4df1 | 0x885a |
| 0x887a | 0x31fd80 | 0x4df9 | 0x887a |
| 0x88e9 | 0x31fdb7 | 0x4e2a | 0x88e9 |
| 0x8911 | 0x31fdcc | 0x50f3 | 0x8911 |
| 0x895e | 0x31fdfa | 0x510c | 0x895e |
| 0x8987 | 0x31fe25 | 0x511d | 0x8987 |
| 0x89e2 | 0x31fe59 | 0x5155 | 0x89e2 |
| 0x89f4 | 0x31fe6d | 0x5250 | 0x89f4 |
| 0x8a96 | 0x31fe9d | 0x529a | 0x8a96 |
| 0x8aae | 0x31febb | 0x52ab | 0x8aae |
| 0x8b0c | 0x31fef6 | 0x52cb | 0x8b0c |
| 0x8bb4 | 0x31ff20 | 0x5528 | 0x8bb4 |
| 0x8bde | 0x31ff46 | 0x55cb | 0x8bde |
| 0x8c63 | 0x31ff58 | 0x56e7 | 0x8c63 |
| 0x8d29 | 0x31ff8b | 0x5813 | 0x8d29 |
| 0x8dba | 0x31ffc3 | 0x58b5 | 0x8dba |
| 0x8e27 | 0x31fff6 | 0x58dd | 0x8e27 |
| 0x8edd | 0x32001f | 0x5b01 | 0x8edd |
| 0x904d | 0x320050 | 0x5ce2 | 0x904d |
| 0x906e | 0x32007a | 0x5cfa | 0x906e |
| 0x909e | 0x3200ae | 0x5d02 | 0x909e |
| 0x916b | 0x3200d7 | 0x5d84 | 0x916b |
| 0x9207 | 0x3200eb | 0x5dbd | 0x9207 |
| 0x9215 | 0x3200ff | 0x5dee | 0x9215 |
| 0x926a | 0x320132 | 0x5e0e | 0x926a |
| 0x92ae | 0x320163 | 0x5e8b | 0x92ae |
| 0x9308 | 0x320192 | 0x5eab | 0x9308 |
| 0x9351 | 0x3201a9 | 0x5edc | 0x9351 |
| 0x93ee | 0x3201d8 | 0x5fe6 | 0x93ee |
| 0x93fb | 0x3201e7 | 0x5ffe | 0x93fb |
| 0x942a | 0x320219 | 0x6006 | 0x942a |
| 0x943c | 0x320231 | 0x6034 | 0x943c |
| 0x9446 | 0x32023c | 0x6045 | 0x9446 |
| 0x9470 | 0x320267 | 0x604d | 0x9470 |
| 0x949b | 0x320297 | 0x60f1 | 0x949b |
| 0x94ff | 0x3202c9 | 0x6174 | 0x94ff |
| 0x953d | 0x3202dd | 0x619d | 0x953d |
| 0x95c0 | 0x3202fc | 0x62d9 | 0x95c0 |
| 0x95e9 | 0x320327 | 0x62e1 | 0x95e9 |
| 0x95f7 | 0x32033b | 0x62f9 | 0x95f7 |
| 0x9639 | 0x320357 | 0x6378 | 0x9639 |
| 0x9666 | 0x320388 | 0x639e | 0x9666 |
| 0x9695 | 0x3203ba | 0x63a6 | 0x9695 |
| 0x96bd | 0x3203e5 | 0x63c4 | 0x96bd |
| 0x973e | 0x3203ed | 0x640d | 0x973e |
| 0x976a | 0x32041a | 0x641e | 0x976a |
| 0x9799 | 0x320451 | 0x6426 | 0x9799 |
| 0x97a8 | 0x320462 | 0x6469 | 0x97a8 |
| 0x97b3 | 0x320470 | 0x6487 | 0x97b3 |
| 0x97d6 | 0x320491 | 0x650a | 0x97d6 |
| 0x985f | 0x3204c5 | 0x653b | 0x985f |
| 0x9889 | 0x3204f2 | 0x6543 | 0x9889 |
| 0x98d6 | 0x32050d | 0x6677 | 0x98d6 |
| 0x9934 | 0x320544 | 0x6690 | 0x9934 |
| 0x99ba | 0x320570 | 0x66d0 | 0x99ba |
| 0x99cb | 0x320584 | 0x66e1 | 0x99cb |
| 0x99fa | 0x3205b8 | 0x66e9 | 0x99fa |
| 0x9a47 | 0x3205e7 | 0x671b | 0x9a47 |
| 0x9a8e | 0x320606 | 0x6734 | 0x9a8e |
| 0x9abb | 0x320635 | 0x673c | 0x9abb |
| 0x9aff | 0x32064d | 0x6775 | 0x9aff |
| 0x9b2c | 0x32067d | 0x677d | 0x9b2c |
| 0x9b58 | 0x3206aa | 0x6785 | 0x9b58 |
| 0x9b68 | 0x3206bb | 0x6802 | 0x9b68 |
| 0x9bb0 | 0x3206d0 | 0x6833 | 0x9bb0 |
| 0x9c50 | 0x3206e1 | 0x68c9 | 0x9c50 |
| 0x9c7f | 0x320713 | 0x68d1 | 0x9c7f |
| 0x9cae | 0x320743 | 0x68d9 | 0x9cae |
| 0x9cdf | 0x32074f | 0x6930 | 0x9cdf |
| 0x9d11 | 0x320783 | 0x6938 | 0x9d11 |
| 0x9d1d | 0x320795 | 0x6997 | 0x9d1d |
| 0x9d4b | 0x3207cd | 0x699f | 0x9d4b |
| 0x9dc9 | 0x3207eb | 0x69e1 | 0x9dc9 |
| 0x9df6 | 0x320820 | 0x69e9 | 0x9df6 |
| 0x9e03 | 0x32082e | 0x6a22 | 0x9e03 |
| 0x9e6b | 0x320857 | 0x6a64 | 0x9e6b |
| 0x9ec2 | 0x320874 | 0x6ad1 | 0x9ec2 |
| 0x9ee8 | 0x32089f | 0x6ae2 | 0x9ee8 |
| 0x9f17 | 0x3208d0 | 0x6aea | 0x9f17 |
| 0x9fa0 | 0x3208ff | 0x6b62 | 0x9fa0 |
| 0xa04e | 0x32092b | 0x6bbf | 0xa04e |
| 0xa0d1 | 0x320948 | 0x6bf8 | 0xa0d1 |
| 0xa117 | 0x32095e | 0x6c3e | 0xa117 |
| 0xa144 | 0x320976 | 0x6cde | 0xa144 |
| 0xa19f | 0x3209a6 | 0x6cee | 0xa19f |
| 0xa1a9 | 0x3209b6 | 0x6d06 | 0xa1a9 |
| 0xa1bb | 0x3209cd | 0x6d26 | 0xa1bb |
| 0xa24c | 0x3209e0 | 0x6e47 | 0xa24c |
| 0xa26f | 0x320a04 | 0x6e4f | 0xa26f |
| 0xa2bb | 0x320a2b | 0x6e7f | 0xa2bb |
| 0xa2f2 | 0x320a51 | 0x6e98 | 0xa2f2 |
| 0xa339 | 0x320a6d | 0x6eb1 | 0xa339 |
| 0xa377 | 0x320a8a | 0x6eca | 0xa377 |
| 0xa37f | 0x320aa2 | 0x6eee | 0xa37f |
| 0xa3a9 | 0x320ab1 | 0x6f10 | 0xa3a9 |
| 0xa3d9 | 0x320ae7 | 0x6f18 | 0xa3d9 |
| 0xa429 | 0x320b15 | 0x6f31 | 0xa429 |
| 0xa47f | 0x320b32 | 0x6f5b | 0xa47f |
| 0xa61b | 0x320b59 | 0x714c | 0xa61b |
| 0xa657 | 0x320b72 | 0x7194 | 0xa657 |
| 0xa67f | 0x320b88 | 0x73bd | 0xa67f |
| 0xa6d4 | 0x320bbc | 0x73d6 | 0xa6d4 |
| 0xa71c | 0x320bc5 | 0x7407 | 0xa71c |
| 0xa768 | 0x320bf8 | 0x7420 | 0xa768 |
| 0xa7c1 | 0x320c2e | 0x7440 | 0xa7c1 |
| 0xa827 | 0x320c62 | 0x748a | 0xa827 |
| 0xa856 | 0x320c97 | 0x7492 | 0xa856 |
| 0xa8f7 | 0x320cbf | 0x7598 | 0xa8f7 |
| 0xa951 | 0x320ceb | 0x75b1 | 0xa951 |
| 0xa97d | 0x320d1a | 0x75b9 | 0xa97d, 0xa98e |
| 0xaaaf | 0x320d39 | 0x76b1 | 0xaaaf |
| 0xaab9 | 0x320d44 | 0x76c9 | 0xaab9 |
| 0xaad3 | 0x320d59 | 0x7739 | 0xaad3 |
| 0xab07 | 0x320d7d | 0x7759 | 0xab07 |
| 0xab3a | 0x320db2 | 0x7761 | 0xab3a |
| 0xab4b | 0x320dcf | 0x7794 | 0xab4b |
| 0xab70 | 0x320df8 | 0x77e8 | 0xab70 |
| 0xabb8 | 0x320e2f | 0x7832 | 0xabb8 |
| 0xabe4 | 0x320e61 | 0x783a | 0xabe4 |
| 0xac65 | 0x320e8e | 0x7862 | 0xac65 |
| 0xac6c | 0x320e97 | 0x788c | 0xac6c |
| 0xacc3 | 0x320ea0 | 0x78ef | 0xacc3 |
| 0xad68 | 0x320ec1 | 0x7973 | 0xad68 |
| 0xade3 | 0x320eea | 0x799b | 0xade3 |
| 0xadf4 | 0x320efc | 0x79c5 | 0xadf4 |
| 0xae10 | 0x320f0d | 0x7a00 | 0xae10 |
| 0xae75 | 0x320f3f | 0x7ada | 0xae75 |
| 0xaeaa | 0x320f78 | 0x7ae2 | 0xaeaa |
| 0xaf09 | 0x320f93 | 0x7be1 | 0xaf09 |
| 0xaf2c | 0x320fbf | 0x7bf2 | 0xaf2c |
| 0xe1c0 | 0x320ff1 | 0xb127 | 0xe1c0, 0xe1da |
| 0xe1df | 0x321013 | 0xb151 | 0xe1df |
| 0xe21f | 0x32104c | 0xb186 | 0xe21f |
| 0xe2b1 | 0x32107a | 0xb1af | 0xe2b1 |
| 0xe2f2 | 0x32108c | 0xb1f8 | 0xe2f2 |
| 0xe351 | 0x3210b8 | 0xb229 | 0xe351 |
| 0xe38f | 0x3210cd | 0xb25b | 0xe38f |
| 0xe40f | 0x3210d9 | 0xb32b | 0xe40f |
| 0xe44c | 0x321109 | 0xb35c | 0xe44c |
| 0xe47a | 0x321138 | 0xb364 | 0xe47a |
| 0xe4d2 | 0x32116b | 0xb38b | 0xe4d2 |
| 0xe525 | 0x32119b | 0xb39b | 0xe525 |
| 0xe612 | 0x3211af | 0xb458 | 0xe612 |
| 0xe666 | 0x3211db | 0xb471 | 0xe666 |
| 0xe696 | 0x32120e | 0xb489 | 0xe696 |
| 0xe7a7 | 0x321244 | 0xb4e2 | 0xe7a7 |
| 0xe80b | 0x32126b | 0xb52d | 0xe80b |
| 0xe89c | 0x32129e | 0xb5bd | 0xe89c |
| 0xe8ad | 0x3212b0 | 0xb5ce | 0xe8ad |
| 0xe962 | 0x3212e2 | 0xb60e | 0xe962 |
| 0xe9bd | 0x32130e | 0xb61e | 0xe9bd |
| 0xea01 | 0x321325 | 0xb63e | 0xea01 |
| 0xeb18 | 0x321353 | 0xb6a0 | 0xeb18 |
| 0xeb47 | 0x321384 | 0xb6a8 | 0xeb47 |
| 0xeba8 | 0x3213ba | 0xb6c8 | 0xeba8 |
| 0xebf8 | 0x3213e8 | 0xb6e8 | 0xebf8 |
| 0xec70 | 0x321410 | 0xb723 | 0xec70 |
| 0xec9f | 0x321445 | 0xb72b | 0xec9f |
| 0xed07 | 0x32147a | 0xb77c | 0xed07 |
| 0xed91 | 0x3214a6 | 0xb7ba | 0xed91 |
| 0xedd9 | 0x3214cb | 0xb7da | 0xedd9 |
| 0xedfe | 0x3214f1 | 0xb7e2 | 0xedfe |
| 0xee42 | 0x321509 | 0xb802 | 0xee42 |
| 0xef0a | 0x321538 | 0xb874 | 0xef0a |
| 0xef44 | 0x32156d | 0xb894 | 0xef44 |
| 0xefd6 | 0x32159c | 0xb8e5 | 0xefd6 |
| 0xf0a7 | 0x3215cb | 0xb927 | 0xf0a7 |
| 0xf0dc | 0x3215fb | 0xb94f | 0xf0dc |
| 0xf1bd | 0x321609 | 0xb9a8 | 0xf1bd |
| 0xf1e4 | 0x321633 | 0xb9c3 | 0xf1e4 |
| 0xf211 | 0x321661 | 0xb9cb | 0xf211 |
| 0xf262 | 0x321685 | 0xba1d | 0xf262 |
| 0xf2f9 | 0x3216ac | 0xba6d | 0xf2f9 |
| 0xf34b | 0x3216d4 | 0xba8d | 0xf34b |
| 0xf396 | 0x321704 | 0xbb2d | 0xf396 |
| 0xf3cd | 0x321734 | 0xbb46 | 0xf3cd |
| 0xf4ae | 0x321762 | 0xbc4e | 0xf4ae |
| 0xf536 | 0x321779 | 0xbc80 | 0xf536 |
| 0xf549 | 0x32178e | 0xbcdb | 0xf549 |
| 0xf573 | 0x3217bd | 0xbce3 | 0xf573 |
| 0xf5c5 | 0x3217ea | 0xbd24 | 0xf5c5 |
| 0xf5ef | 0x321826 | 0xbd3c | 0xf5ef |
| 0xf633 | 0x32184c | 0xbd84 | 0xf633 |
| 0xf665 | 0x321880 | 0xbd8c | 0xf665 |
| 0xf687 | 0x3218a6 | 0xbda4 | 0xf687 |
| 0xf6ab | 0x3218ce | 0xbdd4 | 0xf6ab |
| 0xf709 | 0x321906 | 0xbdf4 | 0xf709 |
| 0xf76d | 0x321927 | 0xbe7e | 0xf76d |
| 0xf7fb | 0x32195c | 0xbea7 | 0xf7fb |
| 0xf844 | 0x321968 | 0xbef9 | 0xf844 |
| 0xf86d | 0x321995 | 0xbf22 | 0xf86d |
| 0xf8e0 | 0x3219b1 | 0xbf5c | 0xf8e0 |
| 0xf8ef | 0x3219c6 | 0xbf74 | 0xf8ef |
| 0xf92d | 0x3219d7 | 0xbf94 | 0xf92d |
| 0xf93f | 0x3219f1 | 0xbfac | 0xf93f |
| 0xf9cf | 0x321a23 | 0xbff7 | 0xf9cf |
| 0xfa03 | 0x321a55 | 0xc02f | 0xfa03 |
| 0xfa47 | 0x321a75 | 0xc04f | 0xfa47 |
| 0xfaca | 0x321aa7 | 0xc087 | 0xfaca |
| 0xfaf7 | 0x321ad6 | 0xc08f | 0xfaf7 |
| 0xfb33 | 0x321b06 | 0xc0ca | 0xfb33 |
| 0xfb61 | 0x321b41 | 0xc0d2 | 0xfb61 |
| 0xfbc0 | 0x321b52 | 0xc10a | 0xfbc0 |
| 0xfbd0 | 0x321b65 | 0xc122 | 0xfbd0 |
| 0xfc3d | 0x321b96 | 0xc153 | 0xfc3d |
| 0xfcf7 | 0x321bc5 | 0xc1ad | 0xfcf7 |
| 0xfd21 | 0x321bf2 | 0xc1be | 0xfd21 |
| 0xfd89 | 0x321c29 | 0xc218 | 0xfd89 |
| 0xfe5a | 0x321c5b | 0xc261 | 0xfe5a |
| 0xfeb0 | 0x321c8a | 0xc271 | 0xfeb0 |
| 0xfebf | 0x321c9e | 0xc289 | 0xfebf |
| 0xfee8 | 0x321cab | 0xc316 | 0xfee8 |
| 0xff15 | 0x321cdd | 0xc327 | 0xff15 |
| 0xff70 | 0x321d10 | 0xc347 | 0xff70 |
| 0xffa0 | 0x321d41 | 0xc34f | 0xffa0 |
| 0xffa9 | 0x321d4b | 0xc360 | 0xffa9 |
| 0xffcb | 0x321d77 | 0xc378 | 0xffcb |
| 0xffe3 | 0x321d89 | 0xc3a8 | 0xffe3 |
| 0xfffd | 0x321daa | 0xc3c0 | 0xfffd |
| 0x100b6 | 0x321dda | 0xc418 | 0x100b6 |
| 0x1012a | 0x321e19 | 0xc461 | 0x1012a |
| 0x10157 | 0x321e52 | 0xc469 | 0x10157 |
| 0x10247 | 0x321e84 | 0xc574 | 0x10247 |
| 0x10286 | 0x321e93 | 0xc5a5 | 0x10286 |
| 0x102b4 | 0x321ecb | 0xc5ad | 0x102b4 |
| 0x102bd | 0x321ed5 | 0xc5be | 0x102bd |
| 0x10323 | 0x321f0c | 0xc601 | 0x10323 |
| 0x10352 | 0x321f49 | 0xc609 | 0x10352 |
| 0x103d4 | 0x321f80 | 0xc6d2 | 0x103d4 |
| 0x103fd | 0x321faa | 0xc6da | 0x103fd |
| 0x10412 | 0x321fc0 | 0xc6eb | 0x10412 |
| 0x10467 | 0x321fef | 0xc73f | 0x10467 |
| 0x1047a | 0x321ff7 | 0xc7f6 | 0x1047a |
| 0x104bd | 0x32202b | 0xc8b9 | 0x104bd |
| 0x10505 | 0x322047 | 0xc8d2 | 0x10505 |
| 0x1052d | 0x322070 | 0xc8f4 | 0x1052d |
| 0x10590 | 0x3220a4 | 0xc90d | 0x10590 |
| 0x105c2 | 0x3220e6 | 0xc915 | 0x105c2 |
| 0x10676 | 0x322106 | 0xc956 | 0x10676 |
| 0x10687 | 0x322118 | 0xc967 | 0x10687 |
| 0x10703 | 0x32214a | 0xc988 | 0x10703 |
| 0x1072e | 0x32217c | 0xc990 | 0x1072e |
| 0x10768 | 0x32218f | 0xc9b0 | 0x10768 |
| 0x1079e | 0x3221ba | 0xc9c9 | 0x1079e |
| 0x107ce | 0x3221eb | 0xc9d1 | 0x107ce |
| 0x107fb | 0x322202 | 0xc9fa | 0x107fb |
| 0x10825 | 0x32222d | 0xca02 | 0x10825 |
| 0x10879 | 0x32223d | 0xca4c | 0x10879 |
| 0x1090b | 0x32224b | 0xcb00 | 0x1090b |
| 0x1095b | 0x322264 | 0xcb72 | 0x1095b |
| 0x10976 | 0x322270 | 0xcbad | 0x10976 |
| 0x109c8 | 0x3222a6 | 0xcbe2 | 0x109c8 |
| 0x109d0 | 0x3222b1 | 0xcbfa | 0x109d0 |
| 0x10a45 | 0x3222be | 0xcc6f | 0x10a45 |
| 0x10a5c | 0x3222de | 0xcc87 | 0x10a5c |
| 0x10b03 | 0x3222f2 | 0xccea | 0x10b03 |
| 0x10b17 | 0x322307 | 0xcd02 | 0x10b17 |
| 0x10b3f | 0x322331 | 0xcd0a | 0x10b3f |
| 0x10b52 | 0x322345 | 0xcd1b | 0x10b52 |
| 0x10b85 | 0x32237d | 0xcd23 | 0x10b85 |
| 0x10bb2 | 0x3223ac | 0xcd65 | 0x10bb2 |
| 0x10bbb | 0x3223b7 | 0xcd7f | 0x10bbb |
| 0x10bea | 0x3223f5 | 0xcd87 | 0x10bea |
| 0x10c63 | 0x322421 | 0xcdb8 | 0x10c63 |
| 0x10ca0 | 0x32244e | 0xcdf9 | 0x10ca0 |
| 0x10d4d | 0x32247f | 0xce74 | 0x10d4d |
| 0x10d88 | 0x3224b4 | 0xce94 | 0x10d88 |
| 0x10dc1 | 0x3224bd | 0xceb4 | 0x10dc1 |
| 0x10def | 0x3224f3 | 0xcecc | 0x10def |
| 0x10e4d | 0x322525 | 0xceec | 0x10e4d |
| 0x10e8f | 0x322536 | 0xcf34 | 0x10e8f |
| 0x10fb1 | 0x322570 | 0xcf95 | 0x10fb1 |
| 0x10fe3 | 0x3225a8 | 0xcfdc | 0x10fe3 |
| 0x10ffd | 0x3225c3 | 0xd006 | 0x10ffd |
| 0x1102c | 0x3225fb | 0xd00e | 0x1102c |
| 0x11057 | 0x32262e | 0xd026 | 0x11057 |
| 0x1105e | 0x322637 | 0xd03e | 0x1105e |
| 0x110a2 | 0x32264e | 0xd088 | 0x110a2 |
| 0x110d0 | 0x322683 | 0xd090 | 0x110d0 |
| 0x110f9 | 0x322692 | 0xd0b0 | 0x110f9 |
| 0x11119 | 0x3226bc | 0xd0c8 | 0x11119 |
| 0x11131 | 0x3226d7 | 0xd0f2 | 0x11131 |
| 0x111a2 | 0x3226e5 | 0xd14d | 0x111a2 |
| 0x112af | 0x322717 | 0xd20c | 0x112af |
| 0x112dd | 0x322746 | 0xd214 | 0x112dd |
| 0x113a9 | 0x322776 | 0xd2a2 | 0x113a9 |
| 0x113d8 | 0x3227a6 | 0xd2ba | 0x113d8 |
| 0x113e7 | 0x3227b6 | 0xd314 | 0x113e7 |
| 0x11465 | 0x3227d3 | 0xd354 | 0x11465 |
| 0x114a3 | 0x322808 | 0xd374 | 0x114a3 |
| 0x114fb | 0x322844 | 0xd394 | 0x114fb |
| 0x11528 | 0x322879 | 0xd39c | 0x11528 |
| 0x11555 | 0x3228a7 | 0xd3a4 | 0x11555 |
| 0x11590 | 0x3228b3 | 0xd3c4 | 0x11590 |
| 0x11615 | 0x3228e7 | 0xd445 | 0x11615 |
| 0x1164e | 0x322917 | 0xd477 | 0x1164e |
| 0x1167e | 0x32294f | 0xd47f | 0x1167e |
| 0x116b4 | 0x322981 | 0xd498 | 0x116b4 |
| 0x11708 | 0x3229b7 | 0xd4a8 | 0x11708 |
| 0x11763 | 0x3229cc | 0xd4eb | 0x11763 |
| 0x11792 | 0x3229fd | 0xd4f3 | 0x11792 |
| 0x11811 | 0x322a2e | 0xd53d | 0x11811 |
| 0x118a4 | 0x322a41 | 0xd58f | 0x118a4 |
| 0x118d0 | 0x322a6e | 0xd597 | 0x118d0 |
| 0x11910 | 0x322a81 | 0xd5c9 | 0x11910 |
| 0x1193d | 0x322ab6 | 0xd5da | 0x1193d |
| 0x11984 | 0x322adb | 0xd5fe | 0x11984 |
| 0x119b0 | 0x322b0d | 0xd630 | 0x119b0 |
| 0x119d2 | 0x322b33 | 0xd648 | 0x119d2 |
| 0x119d9 | 0x322b3c | 0xd660 | 0x119d9 |
| 0x11a1c | 0x322b55 | 0xd692 | 0x11a1c |
| 0x11a26 | 0x322b63 | 0xd6bc | 0x11a26 |
| 0x11b07 | 0x322b97 | 0xd75b | 0x11b07 |
| 0x11b64 | 0x322bce | 0xd78c | 0x11b64 |
| 0x11bee | 0x322bfd | 0xd7dc | 0x11bee |
| 0x11c55 | 0x322c0d | 0xd804 | 0x11c55 |
| 0x11c5d | 0x322c16 | 0xd81c | 0x11c5d |
| 0x11c8e | 0x322c49 | 0xd824 | 0x11c8e |
| 0x11cef | 0x322c7c | 0xd844 | 0x11cef |
| 0x11d5a | 0x322caf | 0xd874 | 0x11d5a |
| 0x11d6b | 0x322cc3 | 0xd885 | 0x11d6b |
| 0x11dc9 | 0x322cfd | 0xd8b7 | 0x11dc9 |
| 0x11e11 | 0x322d13 | 0xd8d7 | 0x11e11 |
| 0x11e40 | 0x322d49 | 0xd8df | 0x11e40 |
| 0x11e4a | 0x322d54 | 0xd909 | 0x11e4a |
| 0x11e98 | 0x322d8a | 0xd929 | 0x11e98 |
| 0x11ea3 | 0x322d96 | 0xd953 | 0x11ea3 |
| 0x11f31 | 0x322dcb | 0xd993 | 0x11f31 |
| 0x11f5f | 0x322e04 | 0xd9ab | 0x11f5f |
| 0x11f7a | 0x322e2e | 0xd9c3 | 0x11f7a |
| 0x11f83 | 0x322e39 | 0xda08 | 0x11f83 |
| 0x11fd8 | 0x322e67 | 0xda28 | 0x11fd8 |
| 0x12059 | 0x322ea1 | 0xda60 | 0x12059 |
| 0x12087 | 0x322ed1 | 0xda68 | 0x12087 |
| 0x12129 | 0x322ee5 | 0xdab0 | 0x12129 |
| 0x12162 | 0x322f1c | 0xdad0 | 0x12162 |
| 0x1218e | 0x322f53 | 0xdad8 | 0x1218e |
| 0x121a8 | 0x322f6e | 0xdaf0 | 0x121a8 |
| 0x121d6 | 0x322fa2 | 0xdaf8 | 0x121d6 |
| 0x12203 | 0x322fd5 | 0xdb00 | 0x12203 |
| 0x12224 | 0x322fec | 0xdb77 | 0x12224 |
| 0x1227c | 0x32301c | 0xdba8 | 0x1227c |
| 0x122d3 | 0x323050 | 0xdbc1 | 0x122d3 |
| 0x12306 | 0x323057 | 0xdbe1 | 0x12306 |
| 0x12320 | 0x323075 | 0xdbf2 | 0x12320 |
| 0x1234c | 0x3230a6 | 0xdbfa | 0x1234c |
| 0x12385 | 0x3230c0 | 0xdc66 | 0x12385 |
| 0x123e4 | 0x3230f4 | 0xdc76 | 0x123e4 |
| 0x123ec | 0x3230fd | 0xdc8e | 0x123ec |
| 0x123fa | 0x32310c | 0xdca6 | 0x123fa |
| 0x1244e | 0x323146 | 0xdcd8 | 0x1244e |
| 0x12481 | 0x32317e | 0xdce0 | 0x12481 |
| 0x124ea | 0x3231b7 | 0xdd11 | 0x124ea |
| 0x12517 | 0x3231e7 | 0xdd19 | 0x12517 |
| 0x1251e | 0x3231f0 | 0xdd43 | 0x1251e |
| 0x1256a | 0x32320e | 0xdd63 | 0x1256a |
| 0x1261f | 0x32321b | 0xde2e | 0x1261f |
| 0x126fa | 0x32324e | 0xdf22 | 0x126fa |
| 0x1274e | 0x32325f | 0xdf85 | 0x1274e |
| 0x127a1 | 0x32327b | 0xdfaf | 0x127a1 |
| 0x127b5 | 0x323295 | 0xdfda | 0x127b5 |
| 0x12859 | 0x3232d8 | 0xe013 | 0x12859 |
| 0x129f2 | 0x323300 | 0xe123 | 0x129f2 |
| 0x12a11 | 0x323327 | 0xe12b | 0x12a11 |
| 0x12a32 | 0x32334e | 0xe155 | 0x12a32 |

## Strings

| offset | tier | bytes | budget | texto |
|---|---|---|---|---|
| 0x3398 | T1_in_place | 13 | 13 | Ngh... ghh... |
| 0x33a6 | T1_in_place | 7 | 7 | Nn...\n |
| 0x33ae | REPOINT_head | 18 | 16 | Esta... quente...? |
| 0x33bf | T1_in_place | 3 | 3 | Nh? |
| 0x33c3 | T1_in_place | 9 | 9 | Q-Quem... |
| 0x33cd | T1_in_place | 15 | 21 | ...me chama...? |
| 0x33e3 | REPOINT_head | 22 | 21 | Espera... eu ainda...! |
| 0x33f9 | REPOINT_head | 32 | 31 | INICIANDO PROCESSO DE DESPERTAR. |
| 0x3419 | REPOINT_head | 46 | 40 | SISTEMAS EM ALERTA. REINICIANDO EM 5 SEGUNDOS. |
| 0x3442 | REPOINT_head | 16 | 13 | ERRO DE SISTEMA. |
| 0x3450 | REPOINT_head | 46 | 40 | PROBLEMA DETECTADO NO PROCESSO DE DESPERTAR.\n |
| 0x3479 | REPOINT_head | 27 | 26 | SUJEITO GRAVEMENTE AFETADO. |
| 0x3494 | REPOINT_head | 33 | 28 | COMANDO DE ABORTAR: CANCELADO. \n |
| 0x34b1 | T1_in_place | 33 | 34 | IMPOSSIVEL ENCERRAR O PROCESSO.\n |
| 0x34d4 | REPOINT_head | 30 | 21 | INICIANDO CONTAGEM REGRESSIVA. |
| 0x34ea | T1_in_place | 36 | 36 | 5, {W75}4, {W75}3, {W80}2, {W80}1... |
| 0x350f | T1_in_place | 134 | 137 | T{W10}E{W10}N{W10}H{W10}A{W10} {W10}U{W10}M{W10} {W10}B{W10}O{W10}M{W10} {W10}D{W10}E{W10}S{W10}P{W10}E{W10}R{W10}T{W10}A{W10}R{W10}-- |
| 0x359d | T1_in_place | 14 | 15 | On... Onde...? |
| 0x35ad | T1_in_place | 17 | 17 | Onde... estou...? |
| 0x35bf | REPOINT_head | 50 | 45 | Acima de mim... uma especie de... teto de pano...? |
| 0x35ed | REPOINT_head | 53 | 49 | Quase nenhuma luz...... Ou so esta escuro la fora...? |
| 0x361f | T1_in_place | 29 | 32 | ...Barulho... Parece... fogo? |
| 0x3640 | T1_in_place | 39 | 41 | U... Argh... Esta tudo... distorcido... |
| 0x366a | REPOINT_head | 17 | 15 | Por que... eu...? |
| 0x367a | T1_in_place | 13 | 14 | Voce acordou? |
| 0x3689 | T1_in_place | 13 | 13 | Ngh... hh...? |
| 0x3697 | REPOINT_head | 9 | 8 | O que...? |
| 0x36a0 | REPOINT_cont | 6 | 4 | Garota |
| 0x36a5 | T1_in_place | 48 | 49 | Como voce esta se sentindo? Nao vi ferimentos,\n |
| 0x36d7 | T1_in_place | 29 | 34 | mas sente dor em algum lugar? |
| 0x36fa | REPOINT_head | 47 | 45 | ...Acho que voce ainda pode estar delirando...? |
| 0x3728 | T1_in_place | 18 | 18 | Quem... e voce...? |
| 0x373b | T1_in_place | 5 | 5 | Ah... |
| 0x3741 | T1_in_place | 48 | 50 | Isso... Bem, como eu explico...? Acho que isso\n |
| 0x3774 | T1_in_place | 42 | 45 | pode ser dificil demais de explicar agora. |
| 0x37a2 | REPOINT_head | 49 | 48 | Bom, enfim... voce lembra de alguma coisa sobre\n |
| 0x37d3 | REPOINT_head | 25 | 21 | o que aconteceu com voce? |
| 0x37e9 | T1_in_place | 6 | 6 | Eu...? |
| 0x37f0 | T1_in_place | 7 | 7 | Argh... |
| 0x37f8 | REPOINT_head | 27 | 24 | Ah--apenas tente relaxar... |
| 0x3811 | T1_in_place | 43 | 49 | Depois eu te conto tudo o que quiser saber. |
| 0x3843 | T1_in_place | 16 | 17 | Ah... entendi... |
| 0x3855 | T1_in_place | 32 | 33 | Isso e... tudo so... um sonho... |
| 0x3877 | T1_in_place | 30 | 31 | Por ora, relaxe... e descanse. |
| 0x3897 | T1_in_place | 11 | 11 | Nn... hh... |
| 0x38a3 | REPOINT_head | 12 | 13 | Boa noite... |
| 0x38b1 | REPOINT_cont | 6 | 5 | Mulher |
| 0x38b7 | REPOINT_head | 46 | 37 | Ai, ai, seu quarto esta uma bagunca de novo... |
| 0x38dd | T1_in_place | 28 | 35 | Ei, ei, Tio! Vim te visitar! |
| 0x3901 | T1_in_place | 50 | 53 | Hehe... E bom voce ficar bem feliz! Porque hoje,\n |
| 0x3937 | T1_in_place | 34 | 39 | vou cozinhar o seu favorito      ! |
| 0x395f | T1_in_place | 43 | 47 | Hmmm... Entao se voce ainda nao casou nem\n |
| 0x398f | REPOINT_head | 47 | 44 | quando estiver bem velho, eu caso com voce, ta? |
| 0x39bc | REPOINT_head | 54 | 51 | Eu me preocupo mesmo... Voce nao precisa ficar aqui.\n |
| 0x39f0 | REPOINT_head | 19 | 17 | Voce sempre pode... |
| 0x3a02 | T1_in_place | 38 | 38 | ...Sabe que pode voltar quando quiser. |
| 0x3a29 | REPOINT_head | 37 | 35 | ...Voce anda tao distante esses dias. |
| 0x3a4d | T1_in_place | 37 | 50 | Antes, parecia que voce vivia atras\n |
| 0x3a80 | REPOINT_head | 28 | 30 | de nos dois o tempo todo...  |
| 0x3a9f | REPOINT_cont | 5 | 3 | Homem |
| 0x3aa3 | T1_in_place | 30 | 31 | ...Entao voce tomou o remedio? |
| 0x3ac3 | T1_in_place | 41 | 47 | Um mundo totalmente novo vai te esperar\n |
| 0x3af3 | REPOINT_head | 30 | 27 | quando voce acordar... Hmhmhm. |
| 0x3b0f | T1_in_place | 41 | 43 | Sim... Voce e o primeiro... e o ultimo... |
| 0x3b3b | T1_in_place | 36 | 38 | Eu nao vou mais fazer isso por voce. |
| 0x3b62 | T1_in_place | 6 | 6 | Certo? |
| 0x3b69 | REPOINT_head | 13 | 12 | Hehe, ta bom. |
| 0x3b76 | T1_in_place | 44 | 48 | E bom voce vir. Promessa de mindinho! Jura\n |
| 0x3ba7 | REPOINT_head | 22 | 16 | e que morra se mentir! |
| 0x3bb8 | T1_in_place | 15 | 15 | E uma promessa. |
| 0x3bc8 | T1_in_place | 5 | 5 | Nn... |
| 0x3bce | T1_in_place | 15 | 18 | E... verdade... |
| 0x3be1 | T1_in_place | 13 | 14 | A promessa... |
| 0x3bf0 | REPOINT_head | 18 | 16 | Tenho que... ir... |
| 0x3c01 | REPOINT_head | 21 | 16 | Ela esta esperando... |
| 0x7da5 | REPOINT_head | 28 | 26 | Ela esta esperando... por... |
| 0x7dc0 | T1_in_place | 10 | 11 | Ah...ha... |
| 0x7dcc | T1_in_place | 7 | 8 | ATCHIM! |
| 0x7dd5 | REPOINT_head | 21 | 20 | Argh... Q-Que frio... |
| 0x7dee | T1_in_place | 6 | 7 | ...Ha? |
| 0x7df6 | REPOINT_head | 34 | 32 | Pisco diante da cena desconhecida. |
| 0x7e17 | T1_in_place | 16 | 17 | O-Onde... estou? |
| 0x7e29 | REPOINT_head | 49 | 48 | Olho ao redor. Arvores, arvores e mais arvores.\n |
| 0x7e5a | T1_in_place | 43 | 46 | E uma floresta, e bem densa ainda por cima. |
| 0x7e89 | T1_in_place | 39 | 48 | Parece que as arvores sem fim engolem\n |
| 0x7eba | T1_in_place | 26 | 33 | todo o resto... ate o som. |
| 0x7edc | REPOINT_head | 31 | 25 | Onde... exatamente eu estou...? |
| 0x7ef6 | T1_in_place | 34 | 41 | Como fui parar num lugar assim...? |
| 0x7f20 | REPOINT_head | 22 | 14 | Por que...? Por que... |
| 0x7f2f | REPOINT_head | 40 | 33 | Vasculho minhas memorias freneticamente. |
| 0x7f51 | T1_in_place | 42 | 46 | Ngh... Nao adianta. Nao lembro. O que eu\n |
| 0x7f80 | REPOINT_head | 28 | 24 | estava fazendo ate agora...? |
| 0x7f99 | T1_in_place | 4 | 4 | Gah! |
| 0x7f9e | REPOINT_head | 51 | 50 | Uma dor subita no pe interrompe meus pensamentos.\n |
| 0x7fd1 | REPOINT_head | 44 | 40 | Olho para baixo e percebo... estou descalco. |
| 0x7ffa | REPOINT_head | 11 | 7 | Por que...? |
| 0x8002 | T1_in_place | 7 | 8 | Atchim! |
| 0x800b | REPOINT_head | 27 | 21 | Ai, que frio de congelar... |
| 0x8021 | REPOINT_head | 26 | 24 | Por que eu... Nao, espera. |
| 0x803a | REPOINT_head | 31 | 30 | Por que estou vestido assim...? |
| 0x8059 | T1_in_place | 43 | 43 | Nesse frio, so com uma camisola fininha...? |
| 0x8085 | T1_in_place | 25 | 26 | Sem nem roupa de baixo... |
| 0x80a0 | T1_in_place | 36 | 45 | A-Argh... "Friozinho"... nem chega\n |
| 0x80ce | REPOINT_head | 19 | 15 | perto de descrever. |
| 0x80de | T1_in_place | 50 | 50 | Olho em volta, desesperado por um jeito de fugir\n |
| 0x8111 | T1_in_place | 11 | 13 | deste frio. |
| 0x811f | REPOINT_head | 48 | 46 | Nenhuma casa, nenhuma placa em lugar nenhum...   |
| 0x814e | T1_in_place | 14 | 14 | Gah... Argh... |
| 0x815d | REPOINT_head | 48 | 47 | Minha cabeca tambem esta latejando... Deve ser\n |
| 0x818d | T1_in_place | 18 | 21 | do estomago vazio. |
| 0x81a3 | T1_in_place | 37 | 38 | Ah, claro. Isso e tudo so um sonho... |
| 0x81ca | REPOINT_head | 50 | 49 | ...Droga, nao adianta. Nao da pra me enganar aqui. |
| 0x81fc | T1_in_place | 39 | 46 | De algum jeito, me recomponho e volto\n |
| 0x822b | REPOINT_head | 14 | 11 | a ficar de pe. |
| 0x8237 | REPOINT_head | 47 | 45 | Por mais que eu tente, isto nao e sonho nenhum. |
| 0x8265 | T1_in_place | 21 | 21 | ...Atchim! Aaa-TCHIM! |
| 0x827b | T1_in_place | 35 | 46 | Argh... Preso neste frio sem nada\n |
| 0x82aa | T1_in_place | 41 | 44 | alem de um robe, e pelado por baixo dele. |
| 0x82d7 | T1_in_place | 43 | 51 | Ainda aguento, mas quando o sol se puser,\n |
| 0x830b | REPOINT_head | 57 | 48 | vou pegar um resfriado na certa. Na pior das hipoteses,\n |
| 0x833c | T1_in_place | 16 | 21 | morro congelado. |
| 0x8352 | T1_in_place | 49 | 51 | Se isto nao e sonho, entao aquela tenda onde eu\n |
| 0x8386 | REPOINT_head | 42 | 37 | estava deve estar em algum lugar por aqui. |
| 0x83ac | REPOINT_head | 49 | 48 | Pensando bem, essa e provavelmente minha melhor\n |
| 0x83dd | REPOINT_head | 14 | 12 | aposta aqui... |
| 0x83ea | REPOINT_head | 49 | 48 | Quero voltar pelo caminho que vim, mas nao faco\n |
| 0x841b | T1_in_place | 16 | 31 | ideia de qual e. |
| 0x843b | T1_in_place | 35 | 49 | O que eu faco? Sigo alguma trilha\n |
| 0x846d | T1_in_place | 42 | 45 | e torco pelo melhor? Ou espero ajuda aqui? |
| 0x849b | T1_in_place | 46 | 48 | Quando se perde, a regra um e ficar parado e\n |
| 0x84cc | T1_in_place | 34 | 34 | esperar ajuda. Mas o problema e... |
| 0x84ef | T1_in_place | 41 | 47 | Nao sei nem se alguem vem me procurar...  |
| 0x851f | T1_in_place | 49 | 49 | Nao da pra esperar um grupo de busca quando nem\n |
| 0x8551 | T1_in_place | 30 | 46 | eu sei o que diabos faco aqui. |
| 0x8580 | T1_in_place | 41 | 43 | Acho que vou ter que arriscar se quiser\n |
| 0x85ac | T1_in_place | 11 | 16 | sair daqui. |
| 0x85bd | T1_in_place | 40 | 46 | Melhor me mexer antes que escureca mais. |
| 0x85ec | T1_in_place | 3 | 4 | Ha? |
| 0x85f1 | T1_in_place | 42 | 47 | Sinto um arrepio na espinha... mas desta\n |
| 0x8621 | T1_in_place | 18 | 23 | vez nao e do frio. |
| 0x8639 | T1_in_place | 35 | 35 | O que...? Senti algo... estranho... |
| 0x865d | T1_in_place | 22 | 22 | ...Uou! Q-Que diabos-- |
| 0x8674 | T1_in_place | 44 | 49 | Ah... e so um passaro... Ufa. Quase me deu\n |
| 0x86a6 | REPOINT_head | 21 | 15 | um ataque do coracao. |
| 0x86b6 | T1_in_place | 28 | 33 | Nada de grave. Que alivio... |
| 0x86d8 | T1_in_place | 40 | 43 | La em cima, os passaros ainda grasnam.\n |
| 0x8704 | T1_in_place | 40 | 45 | Parecem bem agitados com alguma coisa... |
| 0x8732 | T1_in_place | 46 | 47 | ...Esses passaros nao calam a boca. O que os\n |
| 0x8762 | REPOINT_head | 25 | 23 | deixou tao assustados...? |
| 0x877a | REPOINT_head | 9 | 8 | *Arrepio* |
| 0x8783 | T1_in_place | 19 | 21 | ...La esta de novo. |
| 0x8799 | REPOINT_head | 46 | 41 | Sinto como se... algo estivesse me observando. |
| 0x87c3 | REPOINT_head | 32 | 25 | Argh... Estou... passando mal... |
| 0x87dd | REPOINT_head | 42 | 41 | Minha visao embaca e perco o equilibrio.\n |
| 0x8807 | T1_in_place | 44 | 44 | Tropeco nos proprios pes e caio pra frente.  |
| 0x8834 | T1_in_place | 18 | 21 | E nesse instante-- |
| 0x884a | T1_in_place | 5 | 6 | Uou-- |
| 0x8851 | T1_in_place | 6 | 8 | *Zas!* |
| 0x885a | REPOINT_head | 34 | 31 | Ouco logo acima da minha cabeca.\n |
| 0x887a | REPOINT_head | 54 | 46 | Um som violento e estridente, como metal contra metal. |
| 0x88a9 | T1_in_place | 13 | 15 | Q... Q-Que... |
| 0x88b9 | T1_in_place | 39 | 47 | Caido de joelhos, me viro com cautela\n |
| 0x88e9 | REPOINT_head | 20 | 13 | para olhar pra tras. |
| 0x88fa | T1_in_place | 22 | 22 | O que... e... isto...? |
| 0x8911 | REPOINT_head | 45 | 44 | Uma fileira de pontas e gumes afiados, como\n |
| 0x893e | T1_in_place | 28 | 31 | laminas, reluz no ar gelado. |
| 0x895e | REPOINT_head | 42 | 40 | Sao como tesouras... ou talvez um serrote? |
| 0x8987 | REPOINT_head | 51 | 46 | Mas serrotes e tesouras nao chegam perto DAQUILO.\n |
| 0x89b6 | T1_in_place | 30 | 31 | E maior que um braco humano... |
| 0x89d6 | T1_in_place | 10 | 11 | Mas que... |
| 0x89e2 | REPOINT_head | 19 | 17 | O que... e AQUILO!? |
| 0x89f4 | REPOINT_head | 47 | 42 | Seja la o que for, e definitivamente um inseto. |
| 0x8a1f | T1_in_place | 44 | 45 | Mas... essa coisa nao parece nenhum inseto\n |
| 0x8a4d | T1_in_place | 13 | 15 | que eu ja vi. |
| 0x8a5d | T1_in_place | 35 | 42 | E no minimo dez vezes... nao, cem\n |
| 0x8a88 | T1_in_place | 12 | 13 | vezes maior. |
| 0x8a96 | REPOINT_head | 29 | 23 | O que esta... acontecendo...? |
| 0x8aae | REPOINT_head | 58 | 51 | A repulsa cresce dentro de mim, e minha pele se arrepia.\n |
| 0x8ae2 | T1_in_place | 37 | 41 | So quero desviar o olhar dessa coisa. |
| 0x8b0c | REPOINT_head | 41 | 37 | O que eu faco...? O que eu devo fazer...? |
| 0x8b32 | T1_in_place | 18 | 18 | Hh... Ah... Aaah-- |
| 0x8b45 | T1_in_place | 40 | 48 | Sem desviar o olhar, salto do penhasco\n |
| 0x8b76 | T1_in_place | 15 | 15 | a minha frente. |
| 0x8b86 | T1_in_place | 40 | 45 | Sinto aquele corte sobrenatural rasgar\n |
| 0x8bb4 | REPOINT_head | 37 | 33 | o ar logo atras de mim enquanto pulo. |
| 0x8bd6 | T1_in_place | 7 | 7 | Aaaaah! |
| 0x8bde | REPOINT_head | 17 | 15 | Estou... voando!? |
| 0x8bee | T1_in_place | 32 | 42 | Por um momento, deslizo pelo ar. |
| 0x8c19 | T1_in_place | 35 | 46 | Sinto-me bater na encosta e rolar\n |
| 0x8c48 | T1_in_place | 20 | 20 | pela ladeira nevada. |
| 0x8c5d | T1_in_place | 5 | 5 | Guh-- |
| 0x8c63 | REPOINT_head | 50 | 49 | Minhas costas batem com forca no chao. O impacto\n |
| 0x8c95 | T1_in_place | 31 | 32 | me tira o folego, e eu engasgo. |
| 0x8cb6 | T1_in_place | 14 | 14 | Argh... Ghh... |
| 0x8cc5 | T1_in_place | 4 | 4 | Ghh! |
| 0x8cca | T1_in_place | 39 | 48 | Meu corpo grita de dor, mas nao tenho\n |
| 0x8cfb | T1_in_place | 41 | 45 | tempo. Cambaleio de pe e comeco a correr. |
| 0x8d29 | REPOINT_head | 55 | 46 | O que era aquilo, o que era aquilo, o que era aquilo... |
| 0x8d58 | T1_in_place | 23 | 24 | QUE DIABOS ERA AQUILO!? |
| 0x8d71 | T1_in_place | 36 | 41 | Um inseto tao imenso nao existe...\n |
| 0x8d9b | T1_in_place | 21 | 30 | Nao tem como existir! |
| 0x8dba | REPOINT_head | 50 | 46 | Entao isto so pode ser um sonho! Aquilo foi tudo\n |
| 0x8de9 | T1_in_place | 11 | 14 | uma ilusao! |
| 0x8df8 | T1_in_place | 40 | 46 | Basta eu me virar e olhar... e vou ver\n |
| 0x8e27 | REPOINT_head | 40 | 34 | todo mundo sorrindo, esperando por mim-- |
| 0x8e4a | T1_in_place | 16 | 16 | E olho pra tras. |
| 0x8e5b | T1_in_place | 24 | 32 | Aaaaargh! V-V-V-Vai...\n |
| 0x8e7c | T1_in_place | 16 | 19 | Vai me DEVORAR!! |
| 0x8e90 | T1_in_place | 47 | 48 | Comeco a ziguezaguear pra direita e esquerda,\n |
| 0x8ec1 | T1_in_place | 21 | 27 | tentando despista-lo. |
| 0x8edd | REPOINT_head | 48 | 40 | Hh... hh... Q-Quanto eu ainda tenho que correr!? |
| 0x8f06 | T1_in_place | 27 | 28 | E-Eu nao... aguento mais... |
| 0x8f23 | T1_in_place | 31 | 33 | Continuo correndo em frente. \n |
| 0x8f45 | T1_in_place | 6 | 6 | Mas... |
| 0x8f4c | T1_in_place | 5 | 5 | Que-- |
| 0x8f52 | T1_in_place | 28 | 34 | Algo cede sob meu calcanhar. |
| 0x8f75 | T1_in_place | 12 | 14 | Aaaaaaaaagh! |
| 0x8f84 | T1_in_place | 6 | 6 | Ghh... |
| 0x8f8b | T1_in_place | 38 | 50 | Argh... Cai de novo...? Tudo... doi... |
| 0x8fbe | T1_in_place | 40 | 49 | Protejo os olhos com a mao, espiando a\n |
| 0x8ff0 | T1_in_place | 40 | 46 | luz que vem de cima. Parece um buraco... |
| 0x901f | T1_in_place | 39 | 45 | Se foi de la que cai... Deve ter sido\n |
| 0x904d | REPOINT_head | 41 | 32 | um arbusto ou algo escondendo o buraco... |
| 0x906e | REPOINT_head | 51 | 47 | Vai ser dificil, mas se eu escalar a parede aqui,\n |
| 0x909e | REPOINT_head | 40 | 37 | talvez consiga voltar pra superficie...? |
| 0x90c4 | T1_in_place | 37 | 47 | Mas mesmo se eu subir, aquela coisa\n |
| 0x90f4 | T1_in_place | 25 | 27 | vai so me comer. Entao... |
| 0x9110 | T1_in_place | 34 | 44 | Estranhamente, as paredes emitem\n |
| 0x913d | T1_in_place | 40 | 45 | um brilho fraco. E tenue, mas me ajuda\n |
| 0x916b | REPOINT_head | 19 | 14 | a enxergar o lugar. |
| 0x917a | T1_in_place | 37 | 46 | Parece algum tipo de caverna. Ha um\n |
| 0x91a9 | T1_in_place | 41 | 46 | tunel que parece seguir por um bom tempo. |
| 0x91d8 | T1_in_place | 35 | 46 | Bem, se nao posso subir, e melhor\n |
| 0x9207 | REPOINT_head | 19 | 13 | seguir em frente... |
| 0x9215 | REPOINT_head | 50 | 48 | Ainda assim, mesmo com esse brilho fraco, nao da\n |
| 0x9246 | T1_in_place | 35 | 35 | pra ver bem como e mais pra dentro. |
| 0x926a | REPOINT_head | 48 | 47 | Talvez seja mais seguro so esperar aqui quieto\n |
| 0x929a | T1_in_place | 9 | 12 | afinal... |
| 0x92a7 | T1_in_place | 6 | 6 | Ah...! |
| 0x92ae | REPOINT_head | 46 | 37 | ...Aquele barulho... Esta chegando mais perto. |
| 0x92d4 | T1_in_place | 42 | 51 | Se eu ficar por aqui, vai so me cacar...\n |
| 0x9308 | REPOINT_head | 22 | 17 | Nao posso parar agora. |
| 0x931a | T1_in_place | 36 | 42 | Decisao tomada, avanco para dentro\n |
| 0x9345 | T1_in_place | 9 | 11 | do tunel. |
| 0x9351 | REPOINT_head | 46 | 38 | Rrgh... Por que isso esta acontecendo comigo!? |
| 0x9378 | T1_in_place | 25 | 28 | Ngh, ha... ufa... ha...\n |
| 0x9395 | T1_in_place | 38 | 38 | Nao sinto ela... vindo atras de mim... |
| 0x93bc | T1_in_place | 47 | 49 | Finalmente me deixo sentar, exaustao e alivio\n |
| 0x93ee | REPOINT_head | 14 | 12 | tomando conta. |
| 0x93fb | REPOINT_head | 49 | 46 | Ha... Estou a salvo agora... I-Isto... deve ser\n |
| 0x942a | REPOINT_head | 23 | 17 | longe... o bastante...  |
| 0x943c | REPOINT_head | 10 | 9 | *Calafrio* |
| 0x9446 | REPOINT_head | 42 | 41 | Me encolho por instinto. Um frio subito,\n |
| 0x9470 | REPOINT_head | 47 | 42 | desagradavelmente familiar, desce pela espinha. |
| 0x949b | REPOINT_head | 49 | 43 | Meu corpo congela. Nao consigo me mexer, diante\n |
| 0x94c7 | T1_in_place | 28 | 36 | de algo alem da compreensao. |
| 0x94ec | T1_in_place | 15 | 18 | Q... P-P-Por... |
| 0x94ff | REPOINT_head | 19 | 16 | Por que esta AQUI!? |
| 0x9510 | T1_in_place | 43 | 44 | O inseto colossal esta bem na minha frente. |
| 0x953d | REPOINT_head | 30 | 26 | Sera que essa coisa me armou!? |
| 0x9558 | T1_in_place | 36 | 42 | Mas os detalhes... ja nao importam\n |
| 0x9583 | T1_in_place | 5 | 8 | mais. |
| 0x958c | T1_in_place | 6 | 6 | Argh-- |
| 0x9593 | T1_in_place | 44 | 44 | Acontece num instante. Estou de costas pra\n |
| 0x95c0 | REPOINT_head | 42 | 40 | parede, e qualquer fuga e bloqueada pelo\n |
| 0x95e9 | REPOINT_head | 19 | 13 | corpo sinuoso dele. |
| 0x95f7 | REPOINT_head | 27 | 18 | Eu... nao tenho como fugir. |
| 0x960a | T1_in_place | 45 | 46 | Ele rasteja pra frente com cautela, como se\n |
| 0x9639 | REPOINT_head | 48 | 44 | tivesse aprendido a licao das tentativas falhas. |
| 0x9666 | REPOINT_head | 49 | 46 | Ele se inclina, perto o bastante pra me agarrar\n |
| 0x9695 | REPOINT_head | 42 | 39 | com um so estalo das mandibulas... e para. |
| 0x96bd | REPOINT_head | 7 | 6 | *Pingo* |
| 0x96c4 | T1_in_place | 43 | 48 | Algo como saliva pinga das mandibulas dele. |
| 0x96f5 | T1_in_place | 26 | 26 | E aqui... que eu morro...? |
| 0x9710 | T1_in_place | 40 | 45 | Assim... nesta situacao sem sentido...\n |
| 0x973e | REPOINT_head | 44 | 43 | devorado por seja la o que for essa coisa... |
| 0x976a | REPOINT_head | 54 | 46 | As mandibulas do inseto enfim se abrem, escancaradas\n |
| 0x9799 | REPOINT_head | 16 | 14 | pra me devorar.  |
| 0x97a8 | REPOINT_head | 13 | 10 | Estou morto-- |
| 0x97b3 | REPOINT_head | 32 | 29 | *Pingo*... *Pingo*... *Pingo*... |
| 0x97d6 | REPOINT_head | 51 | 48 | O inseto de repente se lanca pro lado sem morder,\n |
| 0x9807 | T1_in_place | 35 | 43 | como se tentasse escapar de algo... |
| 0x9833 | T1_in_place | 29 | 43 | ...e algo desce la do alto,\n |
| 0x985f | REPOINT_head | 44 | 41 | translucido e imenso, como que pra esmagar\n |
| 0x9889 | REPOINT_head | 26 | 17 | tudo o que houver embaixo. |
| 0x989b | T1_in_place | 37 | 43 | Engole o inseto colossal sem esforco. |
| 0x98c7 | T1_in_place | 10 | 14 | Mas que... |
| 0x98d6 | REPOINT_head | 54 | 46 | O que e aquilo...? Q-Que esta... acontecendo agora...? |
| 0x9905 | T1_in_place | 43 | 46 | Vejo o inseto se contorcendo e debatendo,\n |
| 0x9934 | REPOINT_head | 43 | 42 | preso dentro do corpo gelatinoso e viscoso. |
| 0x995f | T1_in_place | 41 | 46 | O inseto ja estava alem da compreensao,\n |
| 0x998e | T1_in_place | 43 | 43 | mas essa coisa... desafia toda logica. E... |
| 0x99ba | REPOINT_head | 19 | 16 | Esta derretendo...? |
| 0x99cb | REPOINT_head | 51 | 46 | A carapaca desse inseto enorme, dura feito metal,\n |
| 0x99fa | REPOINT_head | 46 | 40 | borbulha como se estivesse sendo dissolvida.\n |
| 0x9a23 | T1_in_place | 34 | 35 | Esta se desfazendo dentro do limo. |
| 0x9a47 | REPOINT_head | 30 | 23 | Sera que esta... comendo o...? |
| 0x9a5f | T1_in_place | 45 | 46 | O inseto luta desesperadamente dentro dessa\n |
| 0x9a8e | REPOINT_head | 46 | 44 | criatura amorfa, mas o corpo dele esta quase\n |
| 0x9abb | REPOINT_head | 23 | 20 | completamente digerido. |
| 0x9ad0 | T1_in_place | 45 | 46 | So consigo encarar, atonito, ainda em choque. |
| 0x9aff | REPOINT_head | 47 | 44 | O rosto do inseto vem a tona por um instante,\n |
| 0x9b2c | REPOINT_head | 44 | 43 | mas nao tem mais forca. O vermelho viscoso\n |
| 0x9b58 | REPOINT_head | 16 | 15 | o engole de vez. |
| 0x9b68 | REPOINT_head | 20 | 16 | ...Estou... a salvo? |
| 0x9b79 | T1_in_place | 44 | 47 | Sussurro, em pura gratidao por ainda estar\n |
| 0x9ba9 | T1_in_place | 5 | 6 | vivo. |
| 0x9bb0 | REPOINT_head | 16 | 14 | Eu... sobrevi--! |
| 0x9bbf | T1_in_place | 29 | 46 | Nao consigo conter um grito\n |
| 0x9bee | T1_in_place | 27 | 30 | de alivio... ate perceber.  |
| 0x9c0d | T1_in_place | 37 | 43 | A criatura amorfa incha e se agita,\n |
| 0x9c39 | T1_in_place | 18 | 22 | a pouca distancia. |
| 0x9c50 | REPOINT_head | 49 | 46 | Se ainda estiver com fome depois daquele inseto\n |
| 0x9c7f | REPOINT_head | 47 | 46 | enorme, nao ha razao pra nao vir atras de mim\n |
| 0x9cae | REPOINT_head | 11 | 5 | em seguida. |
| 0x9cb4 | T1_in_place | 31 | 35 | Preciso sair daqui, antes que-- |
| 0x9cd8 | T1_in_place | 6 | 6 | ...Ah! |
| 0x9cdf | REPOINT_head | 51 | 49 | A criatura amorfa comeca a escorrer pra frente...\n |
| 0x9d11 | REPOINT_head | 17 | 11 | na minha direcao. |
| 0x9d1d | REPOINT_head | 55 | 45 | Ela para. So esperando... como se tivesse curiosidade\n |
| 0x9d4b | REPOINT_head | 29 | 22 | de ver o que faco em seguida. |
| 0x9d62 | T1_in_place | 6 | 6 | Ngh... |
| 0x9d69 | T1_in_place | 44 | 47 | Sera que me ouve? Sera que sente vibracoes\n |
| 0x9d99 | T1_in_place | 47 | 47 | no chao? Qualquer movimento brusco, e eu morro. |
| 0x9dc9 | REPOINT_head | 52 | 44 | Sem me mexer. Fico perfeitamente imovel, prendendo\n |
| 0x9df6 | REPOINT_head | 13 | 10 | a respiracao. |
| 0x9e03 | REPOINT_head | 40 | 38 | A superficie viscosa comeca a ondular... |
| 0x9e2a | T1_in_place | 34 | 41 | ...e aos poucos se remodela numa\n |
| 0x9e54 | T1_in_place | 15 | 15 | forma familiar. |
| 0x9e64 | T1_in_place | 6 | 6 | Que--? |
| 0x9e6b | REPOINT_head | 28 | 27 | Minha voz morre na garganta. |
| 0x9e87 | T1_in_place | 54 | 58 | O rosto que surge diante de mim e disforme, viscoso,\n |
| 0x9ec2 | REPOINT_head | 42 | 37 | horrendo... mas inconfundivelmente humano. |
| 0x9ee8 | REPOINT_head | 48 | 46 | Olhos perdidos se fixam em mim. A boca arqueja\n |
| 0x9f17 | REPOINT_head | 46 | 45 | e se abre sem som, como um peixe se afogando\n |
| 0x9f45 | T1_in_place | 6 | 7 | no ar. |
| 0x9f4d | T1_in_place | 22 | 22 | O que... e... voce...? |
| 0x9f64 | T1_in_place | 14 | 14 | ...hh... ih... |
| 0x9f73 | T1_in_place | 44 | 44 | Sera que... esta tentando falar...? So soa\n |
| 0x9fa0 | REPOINT_head | 43 | 42 | como ar escapando--nao consigo entender o\n |
| 0x9fcb | T1_in_place | 8 | 12 | que diz. |
| 0x9fd8 | T1_in_place | 14 | 15 | ...kh... ih... |
| 0x9fe8 | T1_in_place | 45 | 45 | Por reflexo ou curiosidade, me aproximo pra\n |
| 0xa016 | T1_in_place | 32 | 44 | ouvir o que diz... e outra voz\n |
| 0xa043 | T1_in_place | 7 | 10 | ressoa. |
| 0xa04e | REPOINT_head | 28 | 25 | Cubra os olhos e os ouvidos! |
| 0xa068 | T1_in_place | 43 | 48 | O comando rispido e seguido por um objeto\n |
| 0xa099 | T1_in_place | 41 | 42 | cilindrico quicando na pedra entre nos.\n |
| 0xa0c4 | T1_in_place | 8 | 12 | Parece-- |
| 0xa0d1 | REPOINT_head | 21 | 19 | Uma granada...? Gah!? |
| 0xa0e5 | T1_in_place | 37 | 49 | Por instinto, fecho os olhos e tapo\n |
| 0xa117 | REPOINT_head | 23 | 13 | os ouvidos com as maos. |
| 0xa125 | T1_in_place | 29 | 30 | ------------------gghh------! |
| 0xa144 | REPOINT_head | 47 | 43 | Esta claro demais pra ver qualquer coisa, mas\n |
| 0xa170 | T1_in_place | 40 | 46 | sinto o chao tremer como se a criatura\n |
| 0xa19f | REPOINT_head | 15 | 9 | se contorcesse. |
| 0xa1a9 | REPOINT_head | 22 | 17 | Sera... Sera que e...? |
| 0xa1bb | REPOINT_head | 18 | 15 | Um agarrao subito. |
| 0xa1cb | T1_in_place | 6 | 7 | Ha...? |
| 0xa1d3 | T1_in_place | 49 | 49 | Alguem agarra minha mao com uma forca incrivel,\n |
| 0xa205 | T1_in_place | 42 | 45 | e quando tento me soltar, levo uma bronca. |
| 0xa233 | T1_in_place | 20 | 24 | Voce congela depois! |
| 0xa24c | REPOINT_head | 35 | 34 | Meu corpo esta flutuando no ar...\n |
| 0xa26f | REPOINT_head | 38 | 31 | E como se eu estivesse voando de novo. |
| 0xa28f | T1_in_place | 39 | 43 | Abro os olhos, nervoso, e vejo alguem\n |
| 0xa2bb | REPOINT_head | 37 | 36 | saltando a frente, minha mao na dela. |
| 0xa2e0 | T1_in_place | 17 | 17 | E tao rapido...\n |
| 0xa2f2 | REPOINT_head | 27 | 25 | E como se fossemos o vento. |
| 0xa30c | T1_in_place | 31 | 44 | Cortamos o ar, e o vento ruge\n |
| 0xa339 | REPOINT_head | 28 | 13 | passando pelos meus ouvidos. |
| 0xa347 | T1_in_place | 41 | 47 | Minha salvadora olha pra tras, como que\n |
| 0xa377 | REPOINT_head | 23 | 7 | checando se estou bem.  |
| 0xa37f | REPOINT_head | 14 | 11 | Uma... mulher? |
| 0xa38b | T1_in_place | 25 | 29 | Nao... mais pra uma moca? |
| 0xa3a9 | REPOINT_head | 53 | 47 | O rosto dela e lindo, embora curiosamente infantil.\n |
| 0xa3d9 | REPOINT_head | 45 | 36 | Orelhas grandes demais... E uma cauda peluda. |
| 0xa3fe | T1_in_place | 25 | 42 | Ha algo... etereo nela.\n |
| 0xa429 | REPOINT_head | 28 | 18 | Nao consigo desviar o olhar. |
| 0xa43c | T1_in_place | 38 | 45 | Mesmo nesta situacao absurda, parece\n |
| 0xa46a | T1_in_place | 18 | 20 | que o tempo parou. |
| 0xa47f | REPOINT_head | 38 | 33 | Entao, de repente, ela franze a testa. |
| 0xa4a1 | T1_in_place | 48 | 49 | Olho pra tras, sem saber o que ela esta vendo... |
| 0xa4d3 | T1_in_place | 7 | 7 | Aaagh-- |
| 0xa4db | T1_in_place | 47 | 49 | Aquela criatura amorfa avanca, se aproximando\n |
| 0xa50d | T1_in_place | 31 | 42 | de nos como uma onda predadora. |
| 0xa538 | T1_in_place | 41 | 45 | Nesta caverna estreita, nao ha pra onde\n |
| 0xa566 | T1_in_place | 6 | 7 | fugir. |
| 0xa56e | T1_in_place | 19 | 22 | Vai nos alcancar--! |
| 0xa585 | T1_in_place | 31 | 43 | Mas a garota ja viu. Ela saca\n |
| 0xa5b1 | T1_in_place | 31 | 38 | outro cilindro da cintura e o\n |
| 0xa5d8 | T1_in_place | 18 | 20 | joga atras de nos. |
| 0xa5ed | T1_in_place | 37 | 45 | O clarao ofuscante e a explosao vem\n |
| 0xa61b | REPOINT_head | 24 | 17 | quase no mesmo instante. |
| 0xa62d | T1_in_place | 29 | 31 | ------------------rngh------! |
| 0xa64d | T1_in_place | 8 | 9 | Gyaaagh! |
| 0xa657 | REPOINT_head | 21 | 17 | Agora e nossa chance! |
| 0xa669 | T1_in_place | 17 | 21 | Ha... hh... ha... |
| 0xa67f | REPOINT_head | 51 | 38 | Estamos do lado de fora... E-Estou enfim a salvo... |
| 0xa6a6 | T1_in_place | 37 | 45 | Minhas pernas cedem. Desabo na neve\n |
| 0xa6d4 | REPOINT_head | 8 | 7 | do chao. |
| 0xa6dc | T1_in_place | 34 | 45 | Mal acredito que consegui correr\n |
| 0xa70a | T1_in_place | 12 | 17 | tudo aquilo. |
| 0xa71c | REPOINT_head | 50 | 44 | Acho que humanos conseguem qualquer coisa quando\n |
| 0xa749 | T1_in_place | 22 | 30 | a vida esta em jogo... |
| 0xa768 | REPOINT_head | 53 | 45 | A garota tambem esta exausta--nao da pra culpa-la--\n |
| 0xa796 | T1_in_place | 33 | 42 | e se senta, recuperando o folego. |
| 0xa7c1 | REPOINT_head | 51 | 43 | ...Ela salvou minha vida... Eu deveria pelo menos\n |
| 0xa7ed | T1_in_place | 18 | 19 | agradecer direito. |
| 0xa801 | T1_in_place | 33 | 37 | M-Muito obrigado por me salvar... |
| 0xa827 | REPOINT_head | 52 | 46 | Sera que ela me ouviu? Minha garganta esta rouca e\n |
| 0xa856 | REPOINT_head | 39 | 36 | aspera, e nao consigo falar muito alto. |
| 0xa87b | T1_in_place | 30 | 34 | Ela percebe e se vira pra mim. |
| 0xa89e | T1_in_place | 46 | 48 | Tem uma expressao estranha no rosto, como se\n |
| 0xa8cf | T1_in_place | 36 | 39 | tivesse visto algo que nao esperava. |
| 0xa8f7 | REPOINT_head | 43 | 42 | Ah... Vendo o rosto dela assim de novo...\n |
| 0xa922 | T1_in_place | 30 | 46 | Tem mesmo algo de bonito nela. |
| 0xa951 | REPOINT_head | 46 | 43 | Aquela expressao um tanto confusa, tambem...\n |
| 0xa97d | REPOINT_head | 23 | 16 | Nossa, ela e uma graca. |
| 0xa98e | REPOINT_cont | 6 | 4 | Garota |
| 0xa993 | T1_in_place | 33 | 38 | Tem algo de errado com meu rosto? |
| 0xa9ba | T1_in_place | 23 | 24 | A-Ah, nao, nada nao...  |
| 0xa9d3 | T1_in_place | 12 | 14 | Mesmo assim. |
| 0xa9e2 | T1_in_place | 44 | 46 | Tiro os olhos de voce por um so instante e\n |
| 0xaa11 | T1_in_place | 41 | 47 | voce some, mas nunca imaginei uma coisa\n |
| 0xaa41 | T1_in_place | 7 | 10 | dessas. |
| 0xaa4c | T1_in_place | 49 | 50 | Ainda bem que cheguei a tempo, mas no futuro...\n |
| 0xaa7f | T1_in_place | 43 | 47 | acho que prefiro que voce nao me de tanto\n |
| 0xaaaf | REPOINT_head | 10 | 9 | trabalho.  |
| 0xaab9 | REPOINT_head | 20 | 18 | Argh... Me desculpe. |
| 0xaacc | T1_in_place | 6 | 6 | ...Hm? |
| 0xaad3 | REPOINT_head | 35 | 32 | Espera, tirar os olhos de mim...?\n |
| 0xaaf4 | T1_in_place | 10 | 18 | E eu sumi? |
| 0xab07 | REPOINT_head | 52 | 50 | O que ela quer dizer com isso? Ela parece de algum\n |
| 0xab3a | REPOINT_head | 28 | 16 | jeito... familiar, tambem... |
| 0xab4b | REPOINT_head | 40 | 36 | Quer dizer que voce sabe quem eu sou...? |
| 0xab70 | REPOINT_head | 54 | 48 | Se voce sabe quem eu sou, de onde venho, por favor--\n |
| 0xaba1 | T1_in_place | 8 | 8 | me diga. |
| 0xabaa | T1_in_place | 12 | 13 | Ha...? Ah... |
| 0xabb8 | REPOINT_head | 49 | 43 | Quem sou eu? Onde estou? O que era aquela coisa\n |
| 0xabe4 | REPOINT_head | 44 | 41 | que me atacou? O que era--quer dizer, como-- |
| 0xac0e | T1_in_place | 39 | 43 | Ngh... Tento fazer todas as perguntas\n |
| 0xac3a | T1_in_place | 27 | 42 | de uma vez, e nenhuma sai\n |
| 0xac65 | REPOINT_head | 8 | 6 | direito. |
| 0xac6c | REPOINT_head | 8 | 5 | Eu sou-- |
| 0xac72 | T1_in_place | 46 | 46 | A garota fica de pe com um sorriso aflito no\n |
| 0xaca1 | T1_in_place | 30 | 33 | rosto e estende a mao pra mim. |
| 0xacc3 | REPOINT_head | 32 | 28 | E melhor voltarmos por enquanto. |
| 0xace0 | T1_in_place | 40 | 41 | Se voce ficar aqui fora vestido assim,\n |
| 0xad0a | T1_in_place | 32 | 35 | vai acabar pegando um resfriado. |
| 0xad2e | T1_in_place | 11 | 11 | Vestido...? |
| 0xad3a | T1_in_place | 45 | 45 | O ar gelado me atinge de novo de uma vez, e\n |
| 0xad68 | REPOINT_head | 40 | 36 | finalmente lembro o estado em que estou. |
| 0xad8d | T1_in_place | 36 | 41 | Pensando bem, sera que andei mesmo\n |
| 0xadb7 | T1_in_place | 43 | 43 | perambulando por toda esta floresta nesta\n |
| 0xade3 | REPOINT_head | 17 | 16 | coisinha fina...? |
| 0xadf4 | REPOINT_head | 16 | 15 | Ha... Aaa-TCHIM! |
| 0xae04 | T1_in_place | 8 | 11 | ...Hehe. |
| 0xae10 | REPOINT_head | 49 | 47 | Ela solta uma risada, clara como um sino, com o\n |
| 0xae40 | T1_in_place | 41 | 46 | som do meu espirro ecoando pela floresta. |
| 0xae6f | T1_in_place | 5 | 5 | Aqui. |
| 0xae75 | REPOINT_head | 56 | 52 | Ela toma minha mao com seus dedos palidos e delicados,\n |
| 0xaeaa | REPOINT_head | 26 | 25 | e me ajuda a ficar de pe.  |
| 0xaec4 | T1_in_place | 6 | 9 | Vamos. |
| 0xaece | T1_in_place | 7 | 8 | E-Ei... |
| 0xaed7 | T1_in_place | 42 | 49 | Movo a mao de leve, apertando de volta o\n |
| 0xaf09 | REPOINT_head | 43 | 34 | aperto dela. Aquele unico toque de calor... |
| 0xaf2c | REPOINT_head | 49 | 48 | ...Eu nao tinha como saber o que nos aguardava.\n |
| 0xaf5d | T1_in_place | 27 | 33 | Que aquilo era so o comeco. |
| 0xe192 | T1_in_place | 44 | 45 | Ao voltarmos para a tenda, a garota comeca\n |
| 0xe1c0 | REPOINT_head | 26 | 25 | a remexer nas bolsas dela. |
| 0xe1da | REPOINT_cont | 6 | 4 | Garota |
| 0xe1df | REPOINT_head | 56 | 45 | Hmm, tenho certeza de que guardei em algum lugar aqui... |
| 0xe20d | T1_in_place | 11 | 17 | Aha! Achei. |
| 0xe21f | REPOINT_head | 45 | 42 | Eu estava sem saber o que fazer com isto...\n |
| 0xe24a | T1_in_place | 43 | 47 | Realmente nao imaginei que fosse ser util\n |
| 0xe27a | T1_in_place | 6 | 10 | assim. |
| 0xe285 | T1_in_place | 42 | 43 | Com essas palavras, a garota estende uns\n |
| 0xe2b1 | REPOINT_head | 17 | 15 | tecidos dobrados. |
| 0xe2c1 | T1_in_place | 47 | 48 | Aqui, uma muda de roupa. Se continuar andando\n |
| 0xe2f2 | REPOINT_head | 43 | 38 | por ai desse jeito, vai pegar um resfriado. |
| 0xe319 | T1_in_place | 6 | 6 | Hm...? |
| 0xe320 | T1_in_place | 44 | 48 | Parecem bem mais resistentes que as roupas\n |
| 0xe351 | REPOINT_head | 20 | 16 | que eu tinha, mas... |
| 0xe362 | T1_in_place | 38 | 44 | Ahaha, nao faz essa cara! Sao roupas\n |
| 0xe38f | REPOINT_head | 11 | 8 | masculinas. |
| 0xe398 | T1_in_place | 7 | 7 | A-Ah... |
| 0xe3a0 | T1_in_place | 33 | 38 | Bem, vou buscar um pouco de agua. |
| 0xe3c7 | T1_in_place | 43 | 43 | Ah, ela esta tentando me dar privacidade.\n |
| 0xe3f3 | T1_in_place | 19 | 19 | Que gentileza dela. |
| 0xe407 | T1_in_place | 6 | 7 | Eita-- |
| 0xe40f | REPOINT_head | 47 | 44 | Uma rajada de ar gelado entra quando a garota\n |
| 0xe43c | T1_in_place | 4 | 15 | sai. |
| 0xe44c | REPOINT_head | 46 | 45 | C-Caramba, que frio... Ta, se eu ficar nessa\n |
| 0xe47a | REPOINT_head | 50 | 49 | por mais tempo, vou acabar pegando alguma coisa... |
| 0xe4ac | T1_in_place | 33 | 37 | Estendo as roupas que ela me deu. |
| 0xe4d2 | REPOINT_head | 47 | 42 | Mas... esta faltando algo. Uma coisa crucial,\n |
| 0xe4fd | T1_in_place | 30 | 39 | importante. Encaro, incerto,\n |
| 0xe525 | REPOINT_head | 19 | 12 | a cabeca inclinada. |
| 0xe532 | T1_in_place | 28 | 28 | ...Cade a roupa de baixo...? |
| 0xe54f | T1_in_place | 42 | 48 | Viro as roupas do avesso, do lado certo,\n |
| 0xe580 | T1_in_place | 37 | 44 | ate sacudo elas... mas nada de cueca. |
| 0xe5ad | T1_in_place | 42 | 48 | Logico. Ela nao teria milagrosamente uma\n |
| 0xe5de | T1_in_place | 36 | 51 | cueca masculina sobrando por ai...   |
| 0xe612 | REPOINT_head | 43 | 34 | O que significa... que nao tenho escolha... |
| 0xe635 | T1_in_place | 45 | 48 | Como nao tenho escolha, como sou um escravo\n |
| 0xe666 | REPOINT_head | 50 | 47 | dos caprichos do destino, vou ter que ir sem nada. |
| 0xe696 | REPOINT_head | 53 | 48 | N-Nao e como se isto fosse algo que eu QUEIRA fazer!  |
| 0xe6c7 | T1_in_place | 48 | 49 | O homem primitivo ja comecou pelado, entao nao\n |
| 0xe6f9 | T1_in_place | 47 | 50 | surte. Vai ser so mais... arejado que o normal. |
| 0xe72c | T1_in_place | 43 | 44 | Tentando me tranquilizar, comeco a vestir\n |
| 0xe759 | T1_in_place | 29 | 31 | as roupas que ela deu. Mas... |
| 0xe779 | T1_in_place | 43 | 45 | Ta, vamos ver essa calca... Tem um buraco\n |
| 0xe7a7 | REPOINT_head | 38 | 35 | aqui, entao isto deve ser a frente...? |
| 0xe7cb | T1_in_place | 9 | 12 | *Vish*... |
| 0xe7d8 | T1_in_place | 42 | 50 | Bele... Hm. Nao parece nada confortavel... |
| 0xe80b | REPOINT_head | 50 | 42 | Ah, tanto faz. Agora visto essa parte de cima...\n |
| 0xe836 | T1_in_place | 24 | 37 | e amarro com esta faixa? |
| 0xe85c | T1_in_place | 5 | 8 | *Vum* |
| 0xe865 | T1_in_place | 9 | 14 | Pronto... |
| 0xe874 | T1_in_place | 32 | 39 | Sinceramente, essa coisa e bem\n |
| 0xe89c | REPOINT_head | 17 | 16 | desconfortavel... |
| 0xe8ad | REPOINT_head | 49 | 45 | A parte de cima esta meio torta, mas a de baixo\n |
| 0xe8db | T1_in_place | 24 | 38 | tem coisa errada demais. |
| 0xe902 | T1_in_place | 46 | 47 | O jeito que esta esticando nao pode ser bom,\n |
| 0xe932 | T1_in_place | 42 | 47 | e esta... ficando meio arejado la embaixo. |
| 0xe962 | REPOINT_head | 43 | 42 | Como a braguilha abre tao larga, esta bem\n |
| 0xe98d | T1_in_place | 39 | 47 | ventilado. Bem, mais como se deixasse\n |
| 0xe9bd | REPOINT_head | 22 | 18 | o vento entrar direto. |
| 0xe9d0 | T1_in_place | 40 | 48 | O verdadeiro problema e como vou fazer\n |
| 0xea01 | REPOINT_head | 45 | 41 | pra nao mostrar tudo pra alguem sem querer... |
| 0xea2b | T1_in_place | 40 | 51 | Tem problemas serios com estas roupas.\n |
| 0xea5f | T1_in_place | 45 | 49 | Estou a uma rajada de virar um exibicionista. |
| 0xea91 | T1_in_place | 39 | 44 | Algo me diz que isto nao vai dar certo. |
| 0xeabe | T1_in_place | 40 | 47 | Talvez eu deva so explicar e pedir uma\n |
| 0xeaee | T1_in_place | 38 | 41 | cueca emprestada...? Nao, nao, nao da. |
| 0xeb18 | REPOINT_head | 48 | 46 | Mesmo sendo um pedido perfeitamente inocente e\n |
| 0xeb47 | REPOINT_head | 53 | 47 | honesto, um cara nao pode pedir cueca pra uma garota. |
| 0xeb77 | T1_in_place | 38 | 48 | E ela esta emprestando isto por pura\n |
| 0xeba8 | REPOINT_head | 45 | 39 | bondade! Nao posso ficar implorando por mais. |
| 0xebd0 | T1_in_place | 35 | 39 | Nao preciso incomoda-la com isto.\n |
| 0xebf8 | REPOINT_head | 39 | 33 | So preciso de um pouco de criatividade. |
| 0xec1a | T1_in_place | 32 | 48 | Decidido o plano, fico mexendo\n |
| 0xec4b | T1_in_place | 24 | 36 | no tecido mais um tempo. |
| 0xec70 | REPOINT_head | 52 | 46 | Ah, achei. Posso usar este tecido mais grosso como\n |
| 0xec9f | REPOINT_head | 52 | 43 | uma especie de avental, e agora isto pode ser... Hm? |
| 0xeccb | T1_in_place | 8 | 8 | ...Ah... |
| 0xecd4 | T1_in_place | 45 | 50 | Sinto olhos em mim e ergo a vista. Ela esta\n |
| 0xed07 | REPOINT_head | 43 | 42 | ali, encarando... espantada, preocupada e\n |
| 0xed32 | T1_in_place | 11 | 12 | exasperada. |
| 0xed3f | T1_in_place | 38 | 38 | Voce nao esta... de brincadeira, esta? |
| 0xed66 | T1_in_place | 40 | 42 | Vejo algo na expressao dela estremecer\n |
| 0xed91 | REPOINT_head | 36 | 26 | enquanto ela aguarda minha resposta. |
| 0xedac | T1_in_place | 37 | 44 | Argh... aquele olhar dela... E como\n |
| 0xedd9 | REPOINT_head | 37 | 36 | um pai dizendo "nao estou bravo, so\n |
| 0xedfe | REPOINT_head | 23 | 21 | decepcionado com voce". |
| 0xee14 | T1_in_place | 43 | 45 | N-Nao, olha, eu explico! So estou vestido\n |
| 0xee42 | REPOINT_head | 46 | 44 | assim porque nao tinha nenhuma roupa de baixo! |
| 0xee6f | T1_in_place | 32 | 43 | ...A coisa que voce enrolou na\n |
| 0xee9b | T1_in_place | 32 | 42 | cintura agora e um aperyu. Vai\n |
| 0xeec6 | T1_in_place | 11 | 15 | nos ombros. |
| 0xeed6 | T1_in_place | 3 | 4 | Ha? |
| 0xeedb | T1_in_place | 35 | 46 | Voce pos tudo no lado errado para\n |
| 0xef0a | REPOINT_head | 52 | 46 | a parte de cima, tambem... e acho que a calca esta\n |
| 0xef39 | T1_in_place | 10 | 10 | do avesso. |
| 0xef44 | REPOINT_head | 46 | 40 | Do avesso...? Espera, a braguilha esta aqui.\n |
| 0xef6d | T1_in_place | 26 | 34 | Entao isto e a frente, ne? |
| 0xef90 | T1_in_place | 30 | 41 | E por ai que a cauda deveria\n |
| 0xefba | T1_in_place | 9 | 10 | passar... |
| 0xefc5 | T1_in_place | 16 | 16 | Ha...? Cauda...? |
| 0xefd6 | REPOINT_head | 46 | 44 | Sou pego de surpresa. Cauda nao e exatamente\n |
| 0xf003 | T1_in_place | 40 | 43 | algo que se espera ouvir numa conversa\n |
| 0xf02f | T1_in_place | 7 | 13 | normal. |
| 0xf03d | T1_in_place | 39 | 45 | Dou uma olhada e noto algo balancando\n |
| 0xf06b | T1_in_place | 11 | 11 | atras dela. |
| 0xf077 | T1_in_place | 40 | 47 | Algo como uma corda, saindo logo acima\n |
| 0xf0a7 | REPOINT_head | 47 | 44 | do traseiro dela. Algo coberto de pelo, quase\n |
| 0xf0d4 | T1_in_place | 7 | 7 | como... |
| 0xf0dc | REPOINT_head | 13 | 10 | ...uma cauda? |
| 0xf0e7 | T1_in_place | 38 | 46 | Pensando bem, acho que vi isto atras\n |
| 0xf116 | T1_in_place | 39 | 41 | dela enquanto corriamos nas cavernas... |
| 0xf140 | T1_in_place | 33 | 41 | Mas descartei a ideia, e claro.\n |
| 0xf16a | T1_in_place | 36 | 36 | O bom senso diz que isso e ridiculo. |
| 0xf18f | T1_in_place | 39 | 45 | Nao, nao, nao. Nao tem como. Deve ser\n |
| 0xf1bd | REPOINT_head | 41 | 38 | algum tipo de acessorio ou coisa assim... |
| 0xf1e4 | REPOINT_head | 45 | 44 | Enquanto pondero as possibilidades, estendo\n |
| 0xf211 | REPOINT_head | 35 | 27 | a mao e agarro a cauda que balanca. |
| 0xf22d | T1_in_place | 6 | 6 | H-Hgh! |
| 0xf234 | T1_in_place | 40 | 45 | Nossa, isto e impressionante. Parece e\n |
| 0xf262 | REPOINT_head | 38 | 33 | tem o toque de uma cauda de verdade... |
| 0xf284 | T1_in_place | 37 | 46 | E essa textura! E ate macia ao toque. |
| 0xf2b3 | T1_in_place | 23 | 26 | H-Ha! Ah... Q... Que... |
| 0xf2ce | T1_in_place | 38 | 42 | Fofa, macia e sedosa. E uma sensacao\n |
| 0xf2f9 | REPOINT_head | 39 | 37 | incrivel... Daria um cachecol perfeito. |
| 0xf31f | T1_in_place | 36 | 43 | E ate se contorce, mas nao consigo\n |
| 0xf34b | REPOINT_head | 47 | 42 | descobrir se ha algum mecanismo movendo isto... |
| 0xf376 | T1_in_place | 6 | 7 | *Pluf* |
| 0xf37e | T1_in_place | 3 | 3 | Hm? |
| 0xf382 | T1_in_place | 19 | 19 | Ngh... Ghh... Hngh! |
| 0xf396 | REPOINT_head | 47 | 44 | O que e isto? Esta ate ficando todo arrepiado\n |
| 0xf3c3 | T1_in_place | 8 | 9 | agora... |
| 0xf3cd | REPOINT_head | 45 | 41 | Enquanto passo as maos pelo pelo macio, ele\n |
| 0xf3f7 | T1_in_place | 39 | 39 | de repente se infla, como se os pelos\n |
| 0xf41f | T1_in_place | 15 | 16 | ficassem em pe. |
| 0xf430 | T1_in_place | 11 | 12 | Mas que...? |
| 0xf43d | T1_in_place | 45 | 47 | A curiosidade falando mais alto, agarro com\n |
| 0xf46d | T1_in_place | 32 | 38 | as duas maos. E nesse momento... |
| 0xf494 | T1_in_place | 8 | 8 | Ah...!\n |
| 0xf49d | T1_in_place | 11 | 16 | ...Aaaaaah! |
| 0xf4ae | REPOINT_head | 22 | 21 | ...Gah! Q-Que diabos-- |
| 0xf4c4 | T1_in_place | 44 | 48 | O grito dela me assusta, e instintivamente\n |
| 0xf4f5 | T1_in_place | 14 | 19 | solto a cauda. |
| 0xf509 | T1_in_place | 40 | 44 | Olho de volta pra ela, sem saber o que\n |
| 0xf536 | REPOINT_head | 20 | 9 | acabou de acontecer. |
| 0xf549 | REPOINT_head | 46 | 41 | Quando encontro o olhar dela, vejo os ombros\n |
| 0xf573 | REPOINT_head | 44 | 37 | tremendo... e ela esta me encarando furiosa? |
| 0xf599 | T1_in_place | 19 | 23 | E-Ei, o que foi...? |
| 0xf5b1 | T1_in_place | 16 | 19 | O que... foi...? |
| 0xf5c5 | REPOINT_head | 59 | 41 | Encarando friamente, a garota da um passo na minha direcao. |
| 0xf5ef | REPOINT_head | 37 | 34 | O que... voce pensa que esta fazendo? |
| 0xf612 | T1_in_place | 16 | 18 | O que eu... que? |
| 0xf625 | T1_in_place | 11 | 13 | Voce ouviu! |
| 0xf633 | REPOINT_head | 51 | 49 | O que voce esta fazendo, agarrando a cauda de uma\n |
| 0xf665 | REPOINT_head | 37 | 33 | garota assim? Acho que fui bem clara! |
| 0xf687 | REPOINT_head | 39 | 35 | Agarrando uma...? Nao, aquilo foi so... |
| 0xf6ab | REPOINT_head | 55 | 43 | Espera, voce nao quer dizer que isso e... e de verdade? |
| 0xf6d7 | T1_in_place | 40 | 49 | Claro que e! Se esta minha linda cauda\n |
| 0xf709 | REPOINT_head | 32 | 25 | nao e de verdade, entao o que e? |
| 0xf723 | T1_in_place | 18 | 18 | N-Nao, e so que... |
| 0xf736 | T1_in_place | 6 | 6 | Argh-- |
| 0xf73d | T1_in_place | 40 | 47 | Cambaleio pra tras, sentindo uma forca\n |
| 0xf76d | REPOINT_head | 52 | 43 | vinda dela totalmente em desacordo com a aparencia\n |
| 0xf799 | T1_in_place | 5 | 6 | fofa. |
| 0xf7a0 | T1_in_place | 43 | 44 | Ela acaricia a cauda com carinho, como se\n |
| 0xf7cd | T1_in_place | 40 | 45 | tentasse consolar a coisa depois de eu\n |
| 0xf7fb | REPOINT_head | 11 | 6 | mexer nela. |
| 0xf802 | T1_in_place | 42 | 47 | Mas mesmo assim, agarrar minha cauda sem\n |
| 0xf832 | T1_in_place | 15 | 17 | nem um aviso... |
| 0xf844 | REPOINT_head | 44 | 40 | Nao... bem, quer dizer... como eu explico... |
| 0xf86d | REPOINT_head | 27 | 25 | Ela solta um suspiro fundo. |
| 0xf887 | T1_in_place | 44 | 44 | ...Parece que voce honestamente nao sabia,\n |
| 0xf8b4 | T1_in_place | 42 | 43 | entao acho que nao tem jeito. Vou deixar\n |
| 0xf8e0 | REPOINT_head | 20 | 14 | passar por enquanto. |
| 0xf8ef | REPOINT_head | 16 | 14 | Bem... desculpa. |
| 0xf8fe | T1_in_place | 44 | 46 | Mas nao e como se a gente esperasse alguem\n |
| 0xf92d | REPOINT_head | 25 | 17 | ter uma cauda de verdade. |
| 0xf93f | REPOINT_head | 49 | 44 | Quer dizer, os humanos evoluiram dos macacos, e\n |
| 0xf96c | T1_in_place | 43 | 48 | acho que houve casos de evolucao reversa... |
| 0xf99d | T1_in_place | 45 | 49 | A garota me olha estranho, como se quisesse\n |
| 0xf9cf | REPOINT_head | 49 | 44 | responder a minha tentativa atrasada de desculpa. |
| 0xf9fc | T1_in_place | 6 | 6 | ...Hm? |
| 0xfa03 | REPOINT_head | 31 | 22 | ...Sera que estou vendo coisas? |
| 0xfa1a | T1_in_place | 35 | 44 | Um rosto lindo, tracos elegantes,\n |
| 0xfa47 | REPOINT_head | 49 | 44 | e cabelo preto brilhante. E. Nada de errado aqui. |
| 0xfa74 | T1_in_place | 44 | 46 | Ela e uma graca, sem duvida, mas nao e bem\n |
| 0xfaa3 | T1_in_place | 37 | 38 | essa a questao agora. O problema e... |
| 0xfaca | REPOINT_head | 46 | 44 | ...E-Eu nao tinha notado em meio a confusao,\n |
| 0xfaf7 | REPOINT_head | 47 | 41 | mas... aquilo sao tufos de pelo na cabeca dela? |
| 0xfb21 | T1_in_place | 16 | 17 | O que foi agora? |
| 0xfb33 | REPOINT_head | 58 | 45 | Aquelas orelhas grandes... grandes e peludas... se mexem\n |
| 0xfb61 | REPOINT_head | 16 | 13 | por um instante. |
| 0xfb6f | T1_in_place | 30 | 31 | Ah... e... bem, isso e... hum. |
| 0xfb8f | T1_in_place | 48 | 48 | Orelhas e cauda... Ela parece humana, mas sera\n |
| 0xfbc0 | REPOINT_head | 18 | 15 | que e outra coisa? |
| 0xfbd0 | REPOINT_head | 48 | 46 | Nao, espera. Nao posso deixar ela me abandonar\n |
| 0xfbff | T1_in_place | 40 | 44 | por eu fazer perguntas idiotas demais... |
| 0xfc2c | T1_in_place | 14 | 16 | ...Nao e nada. |
| 0xfc3d | REPOINT_head | 46 | 44 | Melhor agir como se eu nao tivesse visto nada. |
| 0xfc6a | T1_in_place | 48 | 48 | Ah, e que eu nao conheco muito bem os costumes\n |
| 0xfc9b | T1_in_place | 33 | 43 | e a etiqueta destas bandas, sabe. |
| 0xfcc7 | T1_in_place | 43 | 47 | Isso e bem evidente so de olhar pra voce.\n |
| 0xfcf7 | REPOINT_head | 44 | 41 | O que voce esta fazendo com essas roupas...? |
| 0xfd21 | REPOINT_head | 54 | 44 | A garota solta um suspirinho diante da minha desculpa. |
| 0xfd4e | T1_in_place | 42 | 48 | De todo jeito, e melhor te vestir direito. |
| 0xfd7f | T1_in_place | 6 | 9 | E-E... |
| 0xfd89 | REPOINT_head | 49 | 42 | Diante das palavras dela, me apresso a desfazer\n |
| 0xfdb4 | T1_in_place | 41 | 45 | os nos. Talvez eu tenha apertado os nos\n |
| 0xfde2 | T1_in_place | 9 | 12 | demais... |
| 0xfdef | T1_in_place | 35 | 44 | Pronto... Ufa... Esse ja desatou.\n |
| 0xfe1c | T1_in_place | 38 | 41 | Agora vou... Ngh... Este tambem esta\n |
| 0xfe46 | T1_in_place | 15 | 19 | bem apertado... |
| 0xfe5a | REPOINT_head | 46 | 45 | Enquanto me atrapalho, a garota se ajoelha e\n |
| 0xfe88 | T1_in_place | 29 | 39 | comeca a desatar os nos com\n |
| 0xfeb0 | REPOINT_head | 19 | 14 | destreza tranquila. |
| 0xfebf | REPOINT_head | 12 | 11 | Fica quieto. |
| 0xfecb | T1_in_place | 19 | 20 | T-Ta bom. Obrigado. |
| 0xfee0 | T1_in_place | 5 | 7 | *Vuf* |
| 0xfee8 | REPOINT_head | 49 | 44 | Nunca imaginei que voce usaria isto como faixa... |
| 0xff15 | REPOINT_head | 50 | 46 | Ela murmura com uma ironia esquisita, voltando a\n |
| 0xff44 | T1_in_place | 41 | 43 | atencao pra faixa que segura minha calca. |
| 0xff70 | REPOINT_head | 48 | 47 | Serio? Bem, e comprido e estreito, entao eu so\n |
| 0xffa0 | REPOINT_head | 9 | 8 | imaginei. |
| 0xffa9 | REPOINT_head | 43 | 33 | Quase nao escuto a resposta murmurada dela. |
| 0xffcb | REPOINT_head | 17 | 15 | E roupa de baixo. |
| 0xffdb | T1_in_place | 6 | 7 | ...Ha? |
| 0xffe3 | REPOINT_head | 32 | 25 | Como eu disse... roupa de baixo. |
| 0xfffd | REPOINT_head | 47 | 43 | Roupa de baixo...? Esta tira comprida de pano\n |
| 0x10029 | T1_in_place | 15 | 18 | deveria ser...? |
| 0x1003c | T1_in_place | 47 | 49 | Como uma coisa tao comprida deveria cobrir...\n |
| 0x1006e | T1_in_place | 39 | 43 | Espera. E uma daquelas tangas de tira!? |
| 0x1009a | T1_in_place | 22 | 27 | Pode-se dizer que sim. |
| 0x100b6 | REPOINT_head | 62 | 47 | Tenho certeza de que voce nao sabia, mas ainda assim, o fato\n |
| 0x100e6 | T1_in_place | 39 | 47 | de voce ter decidido usar como faixa... |
| 0x10116 | T1_in_place | 7 | 8 | Hrgh... |
| 0x1011f | T1_in_place | 7 | 10 | Hehe... |
| 0x1012a | REPOINT_head | 56 | 44 | A garota da uma risadinha do meu desanimo visivel, mas\n |
| 0x10157 | REPOINT_head | 49 | 44 | continua trabalhando, as maos correndo pelo pano. |
| 0x10184 | T1_in_place | 11 | 21 | So falta... |
| 0x1019a | T1_in_place | 46 | 47 | Ela puxa a tira de pano da minha cintura num\n |
| 0x101ca | T1_in_place | 16 | 18 | puxao so. Mas... |
| 0x101dd | T1_in_place | 8 | 10 | ...*Paf* |
| 0x101e8 | T1_in_place | 4 | 4 | Ah-- |
| 0x101ed | T1_in_place | 48 | 48 | Aquela faixa-tanga era a unica coisa segurando\n |
| 0x1021e | T1_in_place | 36 | 40 | minha calca. Se aquilo saiu, entao\n |
| 0x10247 | REPOINT_head | 14 | 11 | naturalmente-- |
| 0x10253 | T1_in_place | 50 | 50 | A calca cai no chao... e "Aquilo" balanca diante\n |
| 0x10286 | REPOINT_head | 55 | 45 | dos olhos dela, oscilando alegremente apesar da falta\n |
| 0x102b4 | REPOINT_head | 9 | 8 | de vento. |
| 0x102bd | REPOINT_head | 54 | 47 | A garota congela diante da emboscada visual, incapaz\n |
| 0x102ed | T1_in_place | 38 | 43 | de tirar os olhos do estranho intruso. |
| 0x10319 | T1_in_place | 7 | 9 | Ola...? |
| 0x10323 | REPOINT_head | 60 | 46 | O rosto, o pescoco, as maos e o corpo da garota aos poucos\n |
| 0x10352 | REPOINT_head | 54 | 45 | ficam vermelhos vivos, como se ela fervesse inteira.\n |
| 0x10380 | T1_in_place | 10 | 11 | E entao... |
| 0x1038c | T1_in_place | 3 | 3 | Ii. |
| 0x10390 | T1_in_place | 3 | 3 | Ii? |
| 0x10394 | T1_in_place | 16 | 17 | IIIIIIIIAAAAAAH! |
| 0x103a6 | T1_in_place | 4 | 4 | Hk-- |
| 0x103ab | T1_in_place | 28 | 40 | Como esse grito sai dela!?\n |
| 0x103d4 | REPOINT_head | 41 | 40 | Fico tonto por um momento, dominado por\n |
| 0x103fd | REPOINT_head | 21 | 20 | aflicao ultrassonica. |
| 0x10412 | REPOINT_head | 46 | 42 | E bem quando ponho as maos sobre os ouvidos,\n |
| 0x1043d | T1_in_place | 33 | 41 | tentando bloquear o grito agudo-- |
| 0x10467 | REPOINT_head | 7 | 6 | *BAQUE* |
| 0x1046e | T1_in_place | 10 | 11 | NNNAAARGH! |
| 0x1047a | REPOINT_head | 51 | 43 | Uma forca terrivel e vingativa me atinge embaixo,\n |
| 0x104a6 | T1_in_place | 22 | 22 | e meu mundo e so dor.  |
| 0x104bd | REPOINT_head | 27 | 26 | Pronto, isso deve ser tudo! |
| 0x104d8 | T1_in_place | 40 | 44 | A garota acena satisfeita, me dando um\n |
| 0x10505 | REPOINT_head | 40 | 39 | tapinha gentil e encorajador nas costas. |
| 0x1052d | REPOINT_head | 51 | 48 | E-Entendi. Entao e assim que se veste de verdade... |
| 0x1055e | T1_in_place | 49 | 49 | Tem outra lacuna na minha memoria, mas consegui\n |
| 0x10590 | REPOINT_head | 65 | 49 | sobreviver ao que quer que tenha acontecido, ao menos. Deve ser\n |
| 0x105c2 | REPOINT_head | 31 | 30 | gracas a todo aquele bom karma. |
| 0x105e1 | T1_in_place | 42 | 47 | Entao e assim que deve ser a sensacao...\n |
| 0x10611 | T1_in_place | 39 | 43 | E facil de me mexer. Bem diferente de\n |
| 0x1063d | T1_in_place | 6 | 8 | antes. |
| 0x10646 | T1_in_place | 47 | 47 | Giro no lugar, tentando ter uma nocao de como\n |
| 0x10676 | REPOINT_head | 17 | 16 | as roupas servem. |
| 0x10687 | REPOINT_head | 49 | 42 | Comparada a isto, a primeira tentativa foi como\n |
| 0x106b2 | T1_in_place | 31 | 35 | me enfiar numa camisa de forca. |
| 0x106d6 | T1_in_place | 34 | 44 | Sem cauda alguma, e sem intencao\n |
| 0x10703 | REPOINT_head | 49 | 42 | de mostrar minha bunda, concordamos em costurar\n |
| 0x1072e | REPOINT_head | 18 | 15 | o buraco da cauda. |
| 0x1073e | T1_in_place | 41 | 41 | Ela fala em ter uma cauda como se fosse\n |
| 0x10768 | REPOINT_head | 42 | 41 | natural, mas parece tranquila com eu nao\n |
| 0x10792 | T1_in_place | 8 | 11 | ter uma. |
| 0x1079e | REPOINT_head | 48 | 47 | Fiquei meio curioso sobre isso... mas acho que\n |
| 0x107ce | REPOINT_head | 22 | 21 | cada um e de um jeito. |
| 0x107e4 | T1_in_place | 18 | 22 | Obrigado por tudo. |
| 0x107fb | REPOINT_head | 42 | 41 | Viro-me pra ela, expressando formalmente\n |
| 0x10825 | REPOINT_head | 15 | 13 | minha gratidao. |
| 0x10833 | T1_in_place | 38 | 44 | Ah, nao, imagina. E a gente teve uns\n |
| 0x10860 | T1_in_place | 24 | 24 | mal-entendidos, entao... |
| 0x10879 | REPOINT_head | 13 | 11 | Bom, entao... |
| 0x10885 | T1_in_place | 44 | 45 | A garota se senta ereta, vira-se pra mim e\n |
| 0x108b3 | T1_in_place | 32 | 39 | anuncia num tom claro e franco.  |
| 0x108db | T1_in_place | 5 | 5 | Kuon. |
| 0x108e1 | T1_in_place | 38 | 41 | Meu nome. Acho que ainda nao te disse. |
| 0x1090b | REPOINT_head | 24 | 22 | Kuon. Esse e o meu nome. |
| 0x10922 | T1_in_place | 18 | 21 | A-Ah, seu nome, e? |
| 0x10938 | T1_in_place | 7 | 7 | Kuon... |
| 0x10940 | T1_in_place | 17 | 26 | E como te chamam? |
| 0x1095b | REPOINT_head | 11 | 10 | Meu nome... |
| 0x10966 | T1_in_place | 14 | 15 | Sim, seu nome. |
| 0x10976 | REPOINT_head | 53 | 42 | As palavras de Kuon mexem com algo na minha mente--\n |
| 0x109a1 | T1_in_place | 16 | 20 | algo importante. |
| 0x109b6 | T1_in_place | 17 | 17 | A-Ah, e, eu sou-- |
| 0x109c8 | REPOINT_head | 10 | 7 | Eu sou...? |
| 0x109d0 | REPOINT_head | 12 | 10 | Eu... sou... |
| 0x109db | T1_in_place | 18 | 18 | Espera... Calma... |
| 0x109ee | T1_in_place | 43 | 47 | Enterro o rosto nas maos e tento resgatar\n |
| 0x10a1e | T1_in_place | 33 | 38 | qualquer memoria. Tem que haver\n |
| 0x10a45 | REPOINT_head | 31 | 22 | alguma coisa, qualquer coisa... |
| 0x10a5c | REPOINT_head | 19 | 15 | Eu sou... Eu sou... |
| 0x10a6c | T1_in_place | 36 | 38 | Mas por algum motivo... nada veio.\n |
| 0x10a93 | T1_in_place | 21 | 26 | Nenhum fim pra frase. |
| 0x10aae | T1_in_place | 40 | 48 | B-Bem, de onde voce veio? Ou talvez...\n |
| 0x10adf | T1_in_place | 35 | 35 | o que voce andou fazendo ate agora? |
| 0x10b03 | REPOINT_head | 20 | 19 | De onde... eu venho? |
| 0x10b17 | REPOINT_head | 41 | 39 | De onde eu venho... De onde eu venho...\n |
| 0x10b3f | REPOINT_head | 19 | 18 | De onde eu venho... |
| 0x10b52 | REPOINT_head | 55 | 50 | As palavras se repetem na minha mente como um mantra,\n |
| 0x10b85 | REPOINT_head | 46 | 44 | mas... nada. Nao consigo pensar alem da nevoa. |
| 0x10bb2 | REPOINT_head | 10 | 8 | Entendo... |
| 0x10bbb | REPOINT_head | 61 | 46 | Da pra ver que Kuon tambem esta preocupada, agora que minha\n |
| 0x10bea | REPOINT_head | 43 | 38 | perda de memoria nao parece tao passageira. |
| 0x10c11 | T1_in_place | 36 | 36 | O que eu andei fazendo ate agora...? |
| 0x10c36 | T1_in_place | 41 | 44 | Conforme o pensamento me ocorre, ergo a\n |
| 0x10c63 | REPOINT_head | 44 | 35 | cabeca de novo, e meu olhar recai sobre ela. |
| 0x10c87 | T1_in_place | 24 | 24 | E verdade, ela estava... |
| 0x10ca0 | REPOINT_head | 48 | 47 | Nao lembro de muita coisa, mas se foi ela quem\n |
| 0x10cd0 | T1_in_place | 30 | 32 | cuidou de mim, entao talvez... |
| 0x10cf1 | T1_in_place | 48 | 54 | Parece que ela notou meu olhar de expectativa.\n |
| 0x10d28 | T1_in_place | 32 | 36 | Quando fala, a voz dela e baixa. |
| 0x10d4d | REPOINT_head | 52 | 47 | Voce estava... desmaiado, sozinho nestas montanhas\n |
| 0x10d7d | T1_in_place | 8 | 10 | remotas. |
| 0x10d88 | REPOINT_head | 8 | 6 | Sozinho? |
| 0x10d8f | T1_in_place | 46 | 49 | Mhm. E... eu nunca mais dormiria bem a noite\n |
| 0x10dc1 | REPOINT_head | 53 | 45 | se simplesmente te deixasse, entao... cuidei de voce. |
| 0x10def | REPOINT_head | 49 | 48 | Entao sinto muito por criar esperanca, mas acho\n |
| 0x10e20 | T1_in_place | 41 | 44 | que e tudo o que sei sobre voce ao certo. |
| 0x10e4d | REPOINT_head | 16 | 11 | Eu... entendo... |
| 0x10e59 | T1_in_place | 9 | 10 | Desculpa. |
| 0x10e64 | T1_in_place | 41 | 42 | Nao, a culpa e minha por criar esperanca. |
| 0x10e8f | REPOINT_head | 57 | 51 | E gentileza sua dizer isso, mas... isto e uma confusao,\n |
| 0x10ec3 | T1_in_place | 43 | 51 | nao e? Nao pensei que fosse acabar assim... |
| 0x10ef7 | T1_in_place | 38 | 41 | Resmungando, Kuon pressiona a mao na\n |
| 0x10f21 | T1_in_place | 36 | 40 | testa e esfrega as temporas com os\n |
| 0x10f4a | T1_in_place | 6 | 8 | dedos. |
| 0x10f53 | T1_in_place | 46 | 50 | E, isto e uma baita confusao. Otimo... o que\n |
| 0x10f86 | T1_in_place | 35 | 42 | e que eu faco numa situacao dessas? |
| 0x10fb1 | REPOINT_head | 55 | 49 | Tudo o que descobri foi que nao faco ideia de quem sou. |
| 0x10fe3 | REPOINT_head | 26 | 25 | A proposito... Onde estou? |
| 0x10ffd | REPOINT_head | 55 | 46 | Voce entenderia se eu dissesse que estamos a oeste de\n |
| 0x1102c | REPOINT_head | 50 | 42 | Kujyuri...? Bem no fundo da Provincia de Shishiri? |
| 0x11057 | REPOINT_head | 8 | 6 | Entendo. |
| 0x1105e | REPOINT_head | 22 | 15 | ...Nao. Nenhuma ideia. |
| 0x1106e | T1_in_place | 6 | 6 | ...Ah. |
| 0x11075 | T1_in_place | 34 | 44 | Descobrir o nome deste lugar nao\n |
| 0x110a2 | REPOINT_head | 52 | 45 | me ajuda nem um pouco, ja que ainda nao faco ideia\n |
| 0x110d0 | REPOINT_head | 14 | 11 | de onde estou. |
| 0x110dc | T1_in_place | 27 | 28 | Tem mais alguma coisa...?\n |
| 0x110f9 | REPOINT_head | 41 | 31 | Algo mais que eu possa perguntar a ela... |
| 0x11119 | REPOINT_head | 26 | 23 | Isso, aquela coisa enorme! |
| 0x11131 | REPOINT_head | 13 | 11 | Coisa enorme? |
| 0x1113d | T1_in_place | 37 | 44 | E, isso mesmo! Aquela coisa de limo\n |
| 0x1116a | T1_in_place | 41 | 45 | viscosa que me atacou. O que era aquilo!? |
| 0x11198 | T1_in_place | 8 | 9 | ...Limo? |
| 0x111a2 | REPOINT_head | 49 | 47 | Kuon inclina a cabeca a principio, confusa, mas\n |
| 0x111d2 | T1_in_place | 30 | 36 | entao algo parece lhe ocorrer. |
| 0x111f7 | T1_in_place | 41 | 44 | Ah, talvez voce esteja falando do Tatari? |
| 0x11224 | T1_in_place | 10 | 10 | Tatari...? |
| 0x1122f | T1_in_place | 39 | 44 | E assim que se chama. E um tipo de...\n |
| 0x1125c | T1_in_place | 18 | 20 | criatura? Eu acho? |
| 0x11271 | T1_in_place | 41 | 45 | Kuon responde, a incerteza clara no tom\n |
| 0x1129f | T1_in_place | 15 | 15 | e na expressao. |
| 0x112af | REPOINT_head | 46 | 45 | Se voce me perguntasse o que e, eu nao teria\n |
| 0x112dd | REPOINT_head | 47 | 37 | uma resposta certa pra te dar, pra ser sincera. |
| 0x11303 | T1_in_place | 40 | 47 | So sei que vive bem no fundo da terra,\n |
| 0x11333 | T1_in_place | 23 | 28 | onde o sol nao alcanca. |
| 0x11350 | T1_in_place | 38 | 48 | E ataca e devora criaturas vivas que\n |
| 0x11381 | T1_in_place | 39 | 39 | entram no covil dele--pra se alimentar. |
| 0x113a9 | REPOINT_head | 47 | 46 | Alem disso, ele nunca morre... e acho que e so. |
| 0x113d8 | REPOINT_head | 15 | 14 | Nunca morre...? |
| 0x113e7 | REPOINT_head | 28 | 21 | Isso. Simplesmente nao pode. |
| 0x113fd | T1_in_place | 47 | 48 | Queime, corte, espanque, mas ele ainda revive\n |
| 0x1142e | T1_in_place | 45 | 45 | na hora. Nao importa o que faca, nao da pra\n |
| 0x1145c | T1_in_place | 6 | 8 | matar. |
| 0x11465 | REPOINT_head | 52 | 48 | Nao, qual e. Nenhuma criatura viva poderia de fato\n |
| 0x11496 | T1_in_place | 12 | 12 | ser imortal. |
| 0x114a3 | REPOINT_head | 59 | 50 | Talvez o corpo e a mente dele sejam so muito resistentes,\n |
| 0x114d6 | T1_in_place | 34 | 36 | e isso torne mais dificil mata-lo? |
| 0x114fb | REPOINT_head | 52 | 44 | Nao, e verdade. Nao importa o que facamos com ele,\n |
| 0x11528 | REPOINT_head | 45 | 44 | ele nunca morre. Nao importa o que se faca,\n |
| 0x11555 | REPOINT_head | 11 | 9 | nem como... |
| 0x1155f | T1_in_place | 48 | 48 | A gente so luta pra afugenta-lo, ou assusta-lo\n |
| 0x11590 | REPOINT_head | 51 | 49 | com luzes e barulhos altos. Isso parece funcionar\n |
| 0x115c2 | T1_in_place | 4 | 5 | bem. |
| 0x115c8 | T1_in_place | 36 | 43 | Entao nem sabemos quantos existem.\n |
| 0x115f4 | T1_in_place | 32 | 32 | Nem muito sobre ele, na verdade. |
| 0x11615 | REPOINT_head | 47 | 42 | Que tipo de monstro e esse? Isso e assustador\n |
| 0x11640 | T1_in_place | 9 | 13 | demais... |
| 0x1164e | REPOINT_head | 55 | 47 | Entao voce teve muita sorte. Se eu tivesse chegado so\n |
| 0x1167e | REPOINT_head | 49 | 46 | um pouco mais tarde, nao sobraria nada de voce,\n |
| 0x116ad | T1_in_place | 3 | 6 | ne? |
| 0x116b4 | REPOINT_head | 53 | 42 | As palavras dela me trazem a mente o inseto enorme,\n |
| 0x116df | T1_in_place | 40 | 40 | engolido inteiro e derretido dentro do\n |
| 0x11708 | REPOINT_head | 20 | 13 | corpo daquela coisa. |
| 0x11716 | T1_in_place | 38 | 46 | Kuon ri, talvez da palidez subita no\n |
| 0x11745 | T1_in_place | 22 | 29 | meu rosto, e continua. |
| 0x11763 | REPOINT_head | 48 | 46 | Nao se preocupe. Fique longe do habitat dele e\n |
| 0x11792 | REPOINT_head | 48 | 47 | se mantenha nas trilhas quando viajar pelo mato. |
| 0x117c2 | T1_in_place | 45 | 49 | Desde que tenha essas regras em mente, voce\n |
| 0x117f4 | T1_in_place | 27 | 28 | raramente vai ter problema. |
| 0x11811 | REPOINT_head | 18 | 17 | R-Raramente, e...? |
| 0x11823 | T1_in_place | 45 | 49 | Entao tudo o que passei--aquilo tudo foi so\n |
| 0x11855 | T1_in_place | 32 | 33 | um azar absurdamente improvavel! |
| 0x11877 | T1_in_place | 35 | 44 | Bem, nunca se sabe. O melhor e so\n |
| 0x118a4 | REPOINT_head | 44 | 43 | aceitar que essas coisas acontecem e lidar\n |
| 0x118d0 | REPOINT_head | 18 | 17 | com elas, eu acho. |
| 0x118e2 | T1_in_place | 44 | 45 | Afinal, uma rajada de vento na hora errada\n |
| 0x11910 | REPOINT_head | 52 | 44 | pode ser tudo o que precisa pra acabar com uma vida. |
| 0x1193d | REPOINT_head | 36 | 28 | Ela diz isso quase com naturalidade. |
| 0x1195a | T1_in_place | 31 | 41 | Nao sei se esse tom pratico e\n |
| 0x11984 | REPOINT_head | 49 | 43 | porque toda aquela confusao ficou pra tras, ou... |
| 0x119b0 | REPOINT_head | 37 | 33 | Bem, o que voce pretende fazer agora? |
| 0x119d2 | REPOINT_head | 8 | 6 | Agora... |
| 0x119d9 | REPOINT_head | 24 | 17 | O que EU posso fazer...? |
| 0x119eb | T1_in_place | 44 | 48 | Ah, desculpa. Acho que essa e uma pergunta\n |
| 0x11a1c | REPOINT_head | 13 | 9 | meio injusta. |
| 0x11a26 | REPOINT_head | 51 | 48 | Como e que voce vai responder uma pergunta dessas\n |
| 0x11a57 | T1_in_place | 30 | 44 | quando nem lembra do proprio\n |
| 0x11a84 | T1_in_place | 5 | 5 | nome? |
| 0x11a8a | T1_in_place | 19 | 28 | E, isso resume bem. |
| 0x11aa7 | T1_in_place | 29 | 32 | Hmm. Bem, se e esse o caso... |
| 0x11ac8 | T1_in_place | 32 | 43 | Algo lhe ocorre, e ela faz uma\n |
| 0x11af4 | T1_in_place | 16 | 18 | sugestao gentil. |
| 0x11b07 | REPOINT_head | 54 | 46 | Talvez isto seja algum tipo de destino. Por que voce\n |
| 0x11b36 | T1_in_place | 41 | 45 | nao me deixa cuidar de voce por um tempo? |
| 0x11b64 | REPOINT_head | 46 | 41 | A ideia bizarra me deixa por um instante sem\n |
| 0x11b8e | T1_in_place | 9 | 10 | palavras. |
| 0x11b99 | T1_in_place | 30 | 37 | Esta garota vai cuidar de mim? |
| 0x11bbf | T1_in_place | 42 | 46 | Ah, nao, eu nao poderia. Mas agradeco a... |
| 0x11bee | REPOINT_head | 15 | 12 | ...Nao, espera. |
| 0x11bfb | T1_in_place | 43 | 46 | Se eu sair por conta propria aqui, ou vou\n |
| 0x11c2a | T1_in_place | 39 | 42 | me perder, ou virar o jantar de algum\n |
| 0x11c55 | REPOINT_head | 8 | 7 | monstro. |
| 0x11c5d | REPOINT_head | 50 | 48 | Ainda estou inseguro, mas ela fez muito por mim.\n |
| 0x11c8e | REPOINT_head | 50 | 48 | Ela nao me trairia agora--nao depois de tudo isso. |
| 0x11cbf | T1_in_place | 44 | 47 | Posso ao menos contar com ela ate entender\n |
| 0x11cef | REPOINT_head | 50 | 48 | o que esta havendo. Vou so aceitar isto como uma\n |
| 0x11d20 | T1_in_place | 10 | 13 | boa sorte. |
| 0x11d2e | T1_in_place | 41 | 43 | ...Entendido. Vou contar com voce, pelo\n |
| 0x11d5a | REPOINT_head | 19 | 16 | menos por um tempo. |
| 0x11d6b | REPOINT_head | 57 | 43 | Kuon sorri gentilmente enquanto inclino a cabeca pra ela. |
| 0x11d97 | T1_in_place | 49 | 49 | Sim, acho que e uma escolha sabia. Obediencia e\n |
| 0x11dc9 | REPOINT_head | 21 | 20 | sempre uma coisa boa. |
| 0x11dde | T1_in_place | 49 | 50 | Ela parece aliviada... Esta bem claro que se eu\n |
| 0x11e11 | REPOINT_head | 53 | 46 | tivesse recusado, provavelmente nao teria me virado\n |
| 0x11e40 | REPOINT_head | 10 | 9 | sozinho... |
| 0x11e4a | REPOINT_head | 53 | 42 | Bem, agora que isso esta resolvido, a gente deveria\n |
| 0x11e75 | T1_in_place | 34 | 34 | ao menos decidir um nome pra voce. |
| 0x11e98 | REPOINT_head | 11 | 10 | ...Um nome? |
| 0x11ea3 | REPOINT_head | 52 | 44 | Bem, voce nao pode ficar sem nome pra sempre. Voce\n |
| 0x11ed0 | T1_in_place | 33 | 41 | nao lembra como te chamam, certo? |
| 0x11efa | T1_in_place | 4 | 7 | E... |
| 0x11f02 | T1_in_place | 46 | 46 | Ela tem razao. Nao ter um nome poderia ficar\n |
| 0x11f31 | REPOINT_head | 56 | 45 | inconveniente, principalmente quando chegarmos a cidade. |
| 0x11f5f | REPOINT_head | 41 | 26 | Ta, qualquer coisa provavelmente serve... |
| 0x11f7a | REPOINT_head | 10 | 8 | Espera ai. |
| 0x11f83 | REPOINT_head | 45 | 38 | Talvez... esta seja uma oportunidade de ouro? |
| 0x11faa | T1_in_place | 43 | 45 | Nao estou feliz por nao ter memorias, mas\n |
| 0x11fd8 | REPOINT_head | 57 | 46 | ISSO significa que tenho basicamente uma folha em branco. |
| 0x12007 | T1_in_place | 41 | 46 | O que nos leva a isto... Posso escolher\n |
| 0x12036 | T1_in_place | 31 | 34 | um nome bem legal e misterioso! |
| 0x12059 | REPOINT_head | 47 | 45 | Talvez meu nome fosse algo sem graca e chato,\n |
| 0x12087 | REPOINT_head | 19 | 16 | antes de tudo isso. |
| 0x12098 | T1_in_place | 44 | 47 | Bem, isso nao e tao ruim. Podia facilmente\n |
| 0x120c8 | T1_in_place | 26 | 36 | ter sido algo ridiculo e\n |
| 0x120ed | T1_in_place | 13 | 15 | vergonhoso... |
| 0x120fd | T1_in_place | 39 | 43 | Quer saber, amnesia nao e tao ruim. E\n |
| 0x12129 | REPOINT_head | 54 | 45 | ate demais! Tenho que tirar o melhor de uma situacao\n |
| 0x12157 | T1_in_place | 5 | 10 | ruim. |
| 0x12162 | REPOINT_head | 54 | 43 | Entao esta e uma oportunidade de verdade. Nao da pra\n |
| 0x1218e | REPOINT_head | 26 | 25 | escolher um nome qualquer. |
| 0x121a8 | REPOINT_head | 51 | 45 | So tenho que pensar num nome legal o bastante pra\n |
| 0x121d6 | REPOINT_head | 50 | 44 | deixar todo mundo com inveja, mas nada de que eu\n |
| 0x12203 | REPOINT_head | 22 | 15 | me arrependa depois... |
| 0x12213 | T1_in_place | 16 | 16 | Ta! Meu nome e-- |
| 0x12224 | REPOINT_head | 47 | 43 | Hmm. Que tipo de nome combinaria mais com voce? |
| 0x12250 | T1_in_place | 38 | 43 | Kuon parece indiferente ao meu braco\n |
| 0x1227c | REPOINT_head | 51 | 39 | dramaticamente estendido, ponderando consigo mesma. |
| 0x122a4 | T1_in_place | 45 | 46 | Uma sensacao ruim surge, e nervoso pergunto\n |
| 0x122d3 | REPOINT_head | 6 | 4 | a ela. |
| 0x122d8 | T1_in_place | 44 | 45 | Ah... voce nao esta... pensando em decidir\n |
| 0x12306 | REPOINT_head | 29 | 25 | o meu novo nome tambem, esta? |
| 0x12320 | REPOINT_head | 48 | 43 | Ela parece surpresa, como se nao fizesse ideia\n |
| 0x1234c | REPOINT_head | 25 | 16 | do que estou perguntando. |
| 0x1235d | T1_in_place | 25 | 26 | Pensando em? E meu dever. |
| 0x12378 | T1_in_place | 12 | 12 | S-Seu dever? |
| 0x12385 | REPOINT_head | 51 | 48 | Um guardiao e essencialmente um pai. Ja que agora\n |
| 0x123b6 | T1_in_place | 37 | 45 | sou sua guardia, e meu dever te dar\n |
| 0x123e4 | REPOINT_head | 8 | 7 | um nome. |
| 0x123ec | REPOINT_head | 14 | 13 | Nao, isso e... |
| 0x123fa | REPOINT_head | 57 | 48 | Qual e... Esta garotinha nao pode honestamente se achar\n |
| 0x1242b | T1_in_place | 19 | 34 | minha mae, pode...? |
| 0x1244e | REPOINT_head | 55 | 50 | Embora, se voce preferir seguir por conta propria sem\n |
| 0x12481 | REPOINT_head | 56 | 47 | mim, entao fique a vontade, tome suas proprias decisoes. |
| 0x124b1 | T1_in_place | 12 | 12 | U... Argh... |
| 0x124be | T1_in_place | 39 | 43 | Como discutir com isso...? Kuon sorri\n |
| 0x124ea | REPOINT_head | 47 | 44 | radiante enquanto eu desabo derrotado, e bate\n |
| 0x12517 | REPOINT_head | 8 | 6 | as maos. |
| 0x1251e | REPOINT_head | 29 | 26 | Entao acho que esta decidido! |
| 0x12539 | T1_in_place | 46 | 48 | *Suspiro*... La se foi a ideia toda do "nome\n |
| 0x1256a | REPOINT_head | 12 | 7 | incrivel"... |
| 0x12572 | T1_in_place | 41 | 44 | No fim, acho que ainda nao tenho voz em\n |
| 0x1259f | T1_in_place | 30 | 31 | nada--nem no meu proprio nome. |
| 0x125bf | T1_in_place | 32 | 35 | Bom, vejamos. Seu novo nome e... |
| 0x125e3 | T1_in_place | 42 | 43 | Kuon inclina a cabeca, olhando pensativa\n |
| 0x1260f | T1_in_place | 12 | 15 | para o teto. |
| 0x1261f | REPOINT_head | 50 | 49 | Apos um momento de silencio, ela murmura algumas\n |
| 0x12651 | T1_in_place | 8 | 10 | silabas. |
| 0x1265c | T1_in_place | 11 | 11 | Ha... ku... |
| 0x12668 | T1_in_place | 8 | 8 | Haku...? |
| 0x12671 | T1_in_place | 17 | 19 | Isso mesmo. Haku. |
| 0x12685 | T1_in_place | 45 | 47 | Ela parece bem orgulhosa disso. Tendo dito,\n |
| 0x126b5 | T1_in_place | 20 | 23 | ela sorri confiante. |
| 0x126cd | T1_in_place | 41 | 44 | Acho que voce deveria se chamar Haku de\n |
| 0x126fa | REPOINT_head | 16 | 7 | agora em diante. |
| 0x12702 | T1_in_place | 7 | 7 | Haku... |
| 0x1270a | T1_in_place | 30 | 42 | Rumino o nome que ela me deu.  |
| 0x12735 | T1_in_place | 24 | 24 | ...Nao e la tao legal... |
| 0x1274e | REPOINT_head | 27 | 25 | ...Voce disse alguma coisa? |
| 0x12768 | T1_in_place | 8 | 9 | *Tremor* |
| 0x12772 | T1_in_place | 40 | 46 | Um leve arrepio me percorre, e um frio\n |
| 0x127a1 | REPOINT_head | 25 | 19 | desce pela minha espinha. |
| 0x127b5 | REPOINT_head | 66 | 50 | Embora Kuon esteja sorrindo tao docemente quanto sempre pra mim,\n |
| 0x127e8 | T1_in_place | 31 | 32 | meu sangue gela por um momento. |
| 0x12809 | T1_in_place | 29 | 33 | Erk! N-Nao, nao disse nada... |
| 0x1282b | T1_in_place | 42 | 45 | Em resposta a minha reacao, Kuon limpa a\n |
| 0x12859 | REPOINT_head | 39 | 38 | garganta com uma tossezinha delicada,\n |
| 0x12880 | T1_in_place | 14 | 19 | falando serio. |
| 0x12894 | T1_in_place | 24 | 31 | E um nome muito ilustre. |
| 0x128b4 | T1_in_place | 36 | 45 | Vem do nome de alguem celebrado em\n |
| 0x128e2 | T1_in_place | 27 | 28 | lendas e historias antigas. |
| 0x128ff | T1_in_place | 9 | 10 | Lendas... |
| 0x1290a | T1_in_place | 24 | 30 | Sim... do Utawarerumono. |
| 0x12929 | T1_in_place | 44 | 49 | Sem memorias nem contexto, nao consigo bem\n |
| 0x1295b | T1_in_place | 35 | 42 | apreciar ou entender o significado. |
| 0x12986 | T1_in_place | 41 | 50 | Mas algo no afeto distante na expressao\n |
| 0x129b9 | T1_in_place | 37 | 43 | dela me diz que e um nome importante. |
| 0x129e5 | T1_in_place | 11 | 12 | Tudo bem... |
| 0x129f2 | REPOINT_head | 38 | 30 | De agora em diante, entao, sou Haku.\n |
| 0x12a11 | REPOINT_head | 38 | 32 | Que me chame assim de agora em diante. |
| 0x12a32 | REPOINT_head | 39 | 30 | Mhm. Fico feliz em ouvir isso, eu acho. |