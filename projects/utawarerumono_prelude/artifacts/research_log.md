# Research Log — Utawarerumono: Prelude to the Fallen

**Status:** reconciled
<!-- trocar pending por reconciled so depois da pesquisa IA+humano conciliada (skill 03). -->

## Fontes Avaliadas

| ID | Fonte | Tier |
|----|-------|------|
| SRC-001 | Corpus do jogo (dialogs.csv, 23.933 textos EN) — mineração de nomes por `kb_phase.py` | 1 |
| SRC-002 | Utawarerumono Wiki (fandom) — página do jogo e elenco: https://utawarerumono.fandom.com/wiki/Utawarerumono:_Prelude_to_the_Fallen | 2 |
| SRC-003 | Site oficial: https://utawarerumono.com/prelude-to-the-fallen | 1 |

## Contribuição humana

human_input: entregue — o usuário indicou o site oficial (SRC-003, Encontrada por: Usuário, que o aprovou como fonte preferida); usuário também indicou a wiki Fandom (SRC-002); o usuário pode somar mais fontes depois

## Notas da IA (Fase 1A)

- Grafias oficiais em inglês (SRC-002/003): Hakuowlo, Eruruu, Aruruu, Camyu — o corpus usa as mesmas.
- Nomes não traduzidos: o corpus os traz já romanizados; a regra é manter.
- Não achei glossário oficial de termos (owlo, Onkamiyamukai etc.) na busca; fica para a pesquisa do usuário.

- SRC-003 lido por inteiro (personagens, lugares, termos). Grafias: Hakuowlo, Eruruu, Aruruu, Yuzuha, Oboro, Dorry, Guraa, Tuskur, Teoro, Sopoku, Camyu, Ulthury, Karulau, Touka, Benawi, Kurou, Nuwangi, Sasante, Kamuchataal; Yamayura, Kenashikourupe, Onkamiyamukai, Kunnekamun, Shakukopolu, Evenkuruga, Onkamiyaryu, Giriyagina, Abh-Kamu; owlo, onkami, Uitsualnemetia, Yaanaun Kami.
- Divergência a decidir: o corpus usa "Evenkurugan" (gentílico) e o site "Evenkuruga" (terra); o corpus usa "Kuuya", "Mukkuru", "Genjimaru" etc. que o site não cobre.

## Reconciliação (Fase 1B)

- Concordância: SRC-002 e SRC-003 (usuário) e a pesquisa da IA apontam as mesmas fontes; Tier 1 (SRC-003, SRC-001) e Tier 2 (SRC-002) presentes.
- SRC-002 lida via API do MediaWiki (a página direta bloqueia o leitor). Páginas lidas: Hakuowlo, Eruruu, Aruruu, Oboro, Yuzuha, Benawi, Kurou, Touka, Karulau, Camyu, Ulthury. Gênero (fonte p/ concordância): Hakuowlo M; Oboro M; Benawi M; Kurou M; Eruruu, Aruruu, Yuzuha, Touka, Karulau, Camyu, Ulthury F.
- Divergência resolvida (Tier 1 prevalece): a wiki grafa Kamyu/Karura/Urutorī; o site oficial e o corpus usam Camyu/Karulau/Ulthury → vale o site oficial/corpus.
- Spoilers: as páginas da wiki revelam enredo posterior (ex.: identidade e passado de Hakuowlo, parentescos de Oboro/Yuzuha, Kuon). Isso vai para `spoiler_ledger.json`, nunca para a prosa visível da KB. Cobertura do jogo-alvo: só o arco do Prelude (corpus).
- Gaps compartilhados (sem fonte nas duas): Kuuya, Mukkuru, Genjimaru, Gachatara, Munto, Hien, Hauenkua, Derihourai, Rakshain, Fumirul e demais; ficam UNSOURCED, só com o que o próprio corpus diz.
