"""skill_base.py — Interface base para skills do pipeline como módulos Python.

Substitui o modelo atual (skills como .md lidos em sessão) por classes Python
com interface formal, gate de entrada e contrato de saída. Os .md existentes
continuam como documentação de processo — o .py é o runtime.

Cada skill:
  1. Declara seus inputs (check_inputs) — gate de entrada automático
  2. Implementa run(project) → dict de artefatos produzidos
  3. É auto-contida: lê project.json, lê artefatos, escreve artefatos

Uso:
    skill = ExtractionSkill()
    problems = skill.check_inputs(root)
    if not problems:
        artifacts = skill.run(root)
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path


class Skill(ABC):
    """Base class para skills do pipeline SDD com código por trás.

    FRONTEIRA cognitivo↔determinístico (valor central do framework): SÓ skills com
    substância de código entram no registry Python. As puramente cognitivas
    (01 discovery, 02 entity_resolution, 03 knowledge_building, 04 glossary, 04b, 05b,
    06b, 06c) permanecem playbooks .md — a IA as executa; não há lógica determinística a
    encapsular. O atributo `kind` torna a fronteira consultável:
      - 'deterministic'        — sem IA (extract, qa-checks, reinsert): testável em CI sem rede.
      - 'cognitive'            — harness determinístico com a IA ISOLADA no miolo (translate).
    """

    #: 'deterministic' | 'cognitive' — categoria da skill (ver docstring da classe).
    kind: str = "deterministic"

    @property
    @abstractmethod
    def skill_id(self) -> str:
        """Identificador único da skill (ex: '00', '01')."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome legível (ex: 'Extraction', 'Discovery')."""

    @property
    def required_inputs(self) -> list[str]:
        """Artefatos necessários antes de rodar (caminhos relativos a project root).

        Subclasses sobrescrevem para declarar dependências.
        Exemplo: ["artifacts/dialogs.csv", "artifacts/entities.csv"]
        """
        return []

    def check_inputs(self, project: Path) -> list[str]:
        """Gate de entrada: retorna lista de problemas (vazia = pode rodar)."""
        project = Path(project)
        problems = []
        if not (project / "project.json").is_file():
            problems.append("project.json não encontrado")
            return problems
        for rel in self.required_inputs:
            if not (project / rel).is_file():
                problems.append(f"artefato obrigatório ausente: {rel}")
        return problems

    @abstractmethod
    def run(self, project: Path, **kwargs) -> dict:
        """Executa a skill. Retorna dict com artefatos produzidos e métricas.

        O retorno deve sempre incluir:
          {"status": "ok" | "error", "artifacts": [...], ...}
        """

    def project_cfg(self, project: Path) -> dict:
        """Lê e retorna o project.json do projeto."""
        return json.loads((Path(project) / "project.json").read_text(encoding="utf-8"))

    def __repr__(self):
        return f"<Skill {self.skill_id}: {self.name}>"
