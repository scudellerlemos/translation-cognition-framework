"""conftest raiz: a CI de push/PR nao instala a stack de ML (torch) -- o gate de busca semantica
do kb_gate vira aviso nos testes. O teste do proprio gate remove a variavel."""
import os

os.environ.setdefault("TCF_ALLOW_NO_ML", "1")
