# Decision Log — Breath of Fire IV

> Só entra aqui decisão ratificada pelo usuário ou fato declarado no `project.json`.
> Uma seção `## ` por decisão: o índice guarda ~300 caracteres por seção.
> Fontes: `research_log.md` (ratificação de 2026-06-21) e `kb_ratified.csv` (2026-10-11).

## Charset e acentos <!-- reveal: safe -->

A tradução usa acento e cedilha (pedido do usuário em 2026-10-11). `project.json` declara
`diacritic_strategy: combining_overlay` e `target_charset_supported: true`: cada letra acentuada
custa 2 bytes. Vale para a caixa de diálogo; a fonte de menu ainda não tem acento.

## Grafia de nomes próprios <!-- reveal: safe -->

Quando as fontes divergem (wiki de fãs, manual, Wikipedia), vale a grafia do corpus do jogo.
Ratificado pelo usuário em 2026-10-11.

## Nome do protagonista: Ryu <!-- reveal: safe -->

Nome personalizável pelo jogador; o padrão canônico é "Ryu". Aparece via control code `[04][00]`
(`[04][01]` = Nina, `[04][02]` = Cray, `[04][05]` = Ershin; conferido na cena `AREAE015`),
nunca como texto literal — não se traduz. Ratificado pelo usuário em 2026-06-21.

## Abbess: manter original <!-- reveal: safe -->

Nome próprio de NPC; manter "Abbess", sem traduzir. Ratificado pelo usuário em 2026-06-21.

## Endless → Eternos <!-- reveal: safe -->

Usar "Eternos" em todo o texto narrativo e diálogo. Ratificado pelo usuário em 2026-06-21.

## Hex → maldição <!-- reveal: safe -->

Usar "maldição" em diálogos e narrativa. Ratificado pelo usuário em 2026-06-21.

## Dragon's Eye → Olho do Dragão <!-- reveal: safe -->

Ratificado pelo usuário em 2026-10-11.

## Sandflier Valley → Vale dos Sandfliers <!-- reveal: safe -->

Ratificado pelo usuário em 2026-10-11.

## Oracle of Wind → Oráculo do Vento <!-- reveal: safe -->

Ratificado pelo usuário em 2026-10-11.

## King of Wyndia → Rei de Wyndia <!-- reveal: safe -->

Ratificado pelo usuário em 2026-10-11.

## Gênero de Elina e Deis: feminino <!-- reveal: safe -->

Confirmado pelo corpus. Resolvido em 2026-06-21.

## Elina e Cray: amiga de infância <!-- reveal: safe -->

Elina é amiga de infância de Cray e prometida ao príncipe de Ludia — nunca "noiva de Cray".
Ratificado pelo usuário em 2026-10-11.

## Registro arcaico: thee/thou → "tu" <!-- reveal: safe -->

Fala arcaica do inglês (thee, thou, art) vira segunda pessoa "tu", consistente dentro da fala
(ex.: "ordeno-te", "eu te invoco"). Ratificado pelo usuário em 2026-10-11.

## Acento que muda a palavra: evitar só em menu <!-- reveal: safe -->

Na caixa de diálogo o acento aparece, então a forma acentuada pode ser usada. Em texto de menu
(fonte sem acento) segue valendo: evitar forma que vira outra palavra sem acento (ex.: "Sê" → "Se").
Ratificado pelo usuário em 2026-10-11; escopo reduzido quando a fonte de diálogo ganhou acento.

## Chamba e Synesta: manter original <!-- reveal: safe -->

Topônimos; manter a grafia do corpus, sem traduzir. Ratificado pelo usuário em 2026-10-11.

## Quem fala com Fou-Lu: "Vossa Majestade" formal, sem arcaísmo <!-- reveal: safe -->

O arcaísmo (tu/vós) é só de Fou-Lu e dos Eternos, como no original; os capítulos dele se passam no presente.
Corte e soldados falam com ele em registro formal moderno: "Vossa Majestade" / "Majestade" / "meu senhor" com verbo e
possessivo em 3ª pessoa ("parece cansado", "seus poderes"), nunca "vós sois" nem "tu". Ratificado pelo usuário em 2026-10-12.
