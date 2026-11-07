"""Armazenamento de metas em SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from cockpit.modulos.metas.models import Goal, VALID_PRIORITIES


class GoalStorage:
    """CRUD de metas em arquivo SQLite local."""

    def __init__(self, db_path: str | Path = "data/metas.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS metas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT DEFAULT '',
                    prazo TEXT,
                    prioridade TEXT NOT NULL DEFAULT 'media',
                    concluida INTEGER NOT NULL DEFAULT 0,
                    criado_em TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _row_to_goal(self, row: sqlite3.Row) -> Goal:
        return Goal(
            id=row["id"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            prazo=row["prazo"],
            prioridade=row["prioridade"],
            concluida=bool(row["concluida"]),
            criado_em=row["criado_em"],
        )

    def criar(self, goal: Goal) -> Goal:
        if not goal.titulo or not goal.titulo.strip():
            raise ValueError("Título é obrigatório.")
        if goal.prioridade not in VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida: {goal.prioridade}")
        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO metas (titulo, descricao, prazo, prioridade, concluida, criado_em)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    goal.titulo.strip(),
                    goal.descricao.strip(),
                    goal.prazo,
                    goal.prioridade,
                    1 if goal.concluida else 0,
                    goal.criado_em or "",
                ),
            )
            conn.commit()
            goal.id = cur.lastrowid
        return goal

    def listar(self, apenas_pendentes: bool = False, apenas_concluidas: bool = False) -> list[Goal]:
        query = "SELECT * FROM metas"
        params: tuple = ()
        if apenas_pendentes and apenas_concluidas:
            raise ValueError("Não é possível filtrar por pendentes e concluídas ao mesmo tempo.")
        if apenas_pendentes:
            query += " WHERE concluida = 0"
        elif apenas_concluidas:
            query += " WHERE concluida = 1"
        query += " ORDER BY criado_em DESC"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_goal(row) for row in rows]

    def buscar_por_id(self, goal_id: int) -> Optional[Goal]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM metas WHERE id = ?", (goal_id,)).fetchone()
        if row is None:
            return None
        return self._row_to_goal(row)

    def concluir(self, goal_id: int) -> Optional[Goal]:
        goal = self.buscar_por_id(goal_id)
        if goal is None:
            return None
        goal.concluida = True
        with self._connect() as conn:
            conn.execute("UPDATE metas SET concluida = 1 WHERE id = ?", (goal_id,))
            conn.commit()
        return goal

    def reabrir(self, goal_id: int) -> Optional[Goal]:
        goal = self.buscar_por_id(goal_id)
        if goal is None:
            return None
        goal.concluida = False
        with self._connect() as conn:
            conn.execute("UPDATE metas SET concluida = 0 WHERE id = ?", (goal_id,))
            conn.commit()
        return goal

    def atualizar(self, goal: Goal) -> Optional[Goal]:
        if self.buscar_por_id(goal.id) is None:
            return None
        if not goal.titulo or not goal.titulo.strip():
            raise ValueError("Título é obrigatório.")
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE metas
                SET titulo = ?, descricao = ?, prazo = ?, prioridade = ?
                WHERE id = ?
                """,
                (
                    goal.titulo.strip(),
                    goal.descricao.strip(),
                    goal.prazo,
                    goal.prioridade,
                    goal.id,
                ),
            )
            conn.commit()
        return goal

    def deletar(self, goal_id: int) -> bool:
        if self.buscar_por_id(goal_id) is None:
            return False
        with self._connect() as conn:
            conn.execute("DELETE FROM metas WHERE id = ?", (goal_id,))
            conn.commit()
        return True

    def contar_por_status(self) -> dict[str, int]:
        total = 0
        pendentes = 0
        concluidas = 0
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM metas").fetchone()
            total = row["c"]
            row = conn.execute("SELECT COUNT(*) AS c FROM metas WHERE concluida = 0").fetchone()
            pendentes = row["c"]
            row = conn.execute("SELECT COUNT(*) AS c FROM metas WHERE concluida = 1").fetchone()
            concluidas = row["c"]
        return {"total": total, "pendentes": pendentes, "concluidas": concluidas}