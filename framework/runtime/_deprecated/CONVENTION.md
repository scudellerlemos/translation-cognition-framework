# _deprecated/ — código supersedido

Pasta de arquivo para código Python que foi **substituído mas mantido por referência histórica**.

## O que vai aqui

- Módulos ou funções que existiam numa versão anterior e foram movidos/reescritos
- Variantes descartadas que podem ser úteis para comparação futura
- Código que foi extraído de um god-module e já não tem lugar no runtime ativo

## O que NÃO vai aqui

- Código em uso (mesmo que legado) — fica nos módulos normais com re-export de compat
- Arquivos de artefatos de pipeline — esses vão para `artifacts/discontinued/<cena>/`
- Histórico de mudanças — esse é papel do git log / commit message

## Convenção

- Nomes de arquivo mantêm o original com prefixo `_old_` (ex.: `_old_model_god_module.py`)
- Cada arquivo começa com um comentário explicando o que substituiu e quando
- Não são importados por nenhum módulo ativo (git grep deve dar zero hits)
- Podem ser apagados a qualquer momento sem impacto no pipeline
