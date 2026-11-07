"""Regras de negócio do módulo Metas."""

from __future__ import annotations

from typing import Optional

from cockpit.modulos.metas.models import Goal
from cockpit.modulos.metas.storage import GoalStorage


class GoalService:
    """Coordena operações de metas entre armazenamento e interface."""

    def __init__(self, storage: GoalStorage) -> None:
        self.storage = storage

    def criar_meta(self, titulo: str, descricao: str = "", prazo: str | None = None, prioridade: str = "media") -> Goal:
        goal = Goal(titulo=titulo, descricao=descricao, prazo=prazo, prioridade=prioridade)
        return self.storage.criar(goal)

    def listar_metas(self, apenas_pendentes: bool = False, apenas_concluidas: bool = False) -> list[Goal]:
        return self.storage.listar(apenas_pendentes=apenas_pendentes, apenas_concluidas=apenas_concluidas)

    def concluir_meta(self, goal_id: int) -> Optional[Goal]:
        return self.storage.concluir(goal_id)

    def reabrir_meta(self, goal_id: int) -> Optional[Goal]:
        return self.storage.reabrir(goal_id)

    def atualizar_meta(self, goal: Goal) -> Optional[Goal]:
        return self.storage.atualizar(goal)

    def deletar_meta(self, goal_id: int) -> bool:
        return self.storage.deletar(goal_id)

    def resumo(self) -> dict[str, int]:
        return self.storage.contar_por_status()