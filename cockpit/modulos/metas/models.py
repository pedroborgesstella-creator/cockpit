"""Entidade Goal — representa uma meta pessoal."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


VALID_PRIORITIES = {"baixa", "media", "alta"}


@dataclass
class Goal:
    id: Optional[int] = None
    titulo: str = ""
    descricao: str = ""
    prazo: Optional[str] = None  # YYYY-MM-DD
    prioridade: str = "media"
    concluida: bool = False
    criado_em: Optional[str] = None

    def __post_init__(self) -> None:
        if self.prioridade not in VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida: {self.prioridade}. Use: {', '.join(sorted(VALID_PRIORITIES))}")
        if self.criado_em is None:
            self.criado_em = datetime.now().isoformat(timespec="seconds")

    def esta_concluida(self) -> bool:
        return self.concluida is True

    def resumo(self) -> str:
        status = "[x]" if self.concluida else "[ ]"
        prazo = f" | prazo: {self.prazo}" if self.prazo else ""
        prio = f" | prioridade: {self.prioridade}"
        return f"{status} #{self.id} {self.titulo}{prio}{prazo}"