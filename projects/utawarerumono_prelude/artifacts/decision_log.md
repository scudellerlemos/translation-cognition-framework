# Decision Log — Utawarerumono: Prelude to the Fallen

## Convenções gerais

[Descrever as convenções gerais de tradução adotadas para este projeto.]

## Nomes próprios

[Listar decisões sobre nomes próprios: verbatim ou traduzir, razão.]

## Traduções canônicas

[Listar termos com tradução canônica fixada e o porquê da escolha.]

## Acentos pt-BR (fonte)

- Decisão do usuário: estender a fonte (não transliterar). Implementado e aprovado in-game: acentos desenhados no 
  `font.tex` original + entradas reaproveitadas na tabela ENG do exe (`connector/font.py`, table_schema.md Seção 5);
  patch global de fonte (Font.fnt) descartado: mudava a fonte de tudo. Plano B (transliterar) segue disponível.

## Escopo e caminho

- Caminho: in-session (hitl choose-path, Felipe). Escopo: `completo` = cenas (ScriptTextData) + NameTextData + 
  SysMessageTextData + UnitTextData (349 membros, 23.933 strings). StageTextData fora: o ponteiro EN do próprio jogo 
  aponta para o meio da string. Decisão do usuário: "é sessao, entao é compelto".

## Decisões de voz (Fase 1, 2026-10-14, usuário)

- Nomes de personagens e lugares: mantidos como no jogo (grafia do site oficial SRC-003; Camyu, Karulau, Ulthury, não Kamyu/Karura).
- `owlo` e `onkami`: mantidos sem tradução.
- Tratamento: Lord/Lady → Senhor/Senhora; Your Majesty → Majestade; Big Sis → Irmã mais velha/Mana conforme o caso.
- Registro: corte e guerreiros (Benawi, Ulthury, Touka) formais e solenes sem arcaísmo pesado ("vós" só em cerimônia); aldeões e crianças coloquiais.
- Gênero (usuário): Dorry, Guraa e Sasante masculinos; Kamuchataal feminino.
- Sotaque/dialeto (usuário): nenhum; povos e nações usam o mesmo registro. A variação vem do indivíduo (tiques de fala) e do status social (realeza mais formal que aldeões). Os exemplos do texto colado (Kuuya como imperatriz, tique de Aruruu) não têm fonte nas SRC-001..003: confirmar na leitura das cenas antes de virar regra.
- Gentílico (usuário): Evenkurugan → evenkurugano/evenkurugana, minúscula; a terra segue Evenkuruga. O texto colado chama Karulau de evenkuruguana, mas o site oficial (SRC-003) a dá como Giriyagina e Touka como Evenkuruga: vale a fonte. Giriyaginan → giriyaginano/giriyaginana (usuário, mesmo critério).
- Pendentes antes do piloto: nenhum.

## Interjeições e onomatopeias (onda 2, 2026-10-14, usuário)

- Não ficam no glossário: o alvo `(adaptar)` (23 entradas) era marcador, não tradução, e reprovava qualquer
  forma localizada no `glossary_lint` (e o schema não aceita `traduzir` sem alvo).
- Regra: adaptar à interjeição natural em pt-BR, mantendo o comprimento e o alongamento da fala original;
  a escolha é livre por contexto, sem forma fixa.
- Melhoria do framework (marcador de adaptação livre no schema/lint/migrate) anotada no ROADMAP do projeto.

## Lore da onda +1 (2026-10-15, usuário)

- Tsetse Grass → "Erva Tsetse" (traduz o genérico, mantém o nome próprio). "Gran Tuskur" do levantamento é falso positivo (fala cortada "Gran--" + Tuskur, já no glossário).
