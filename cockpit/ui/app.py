"""TUI rústica estilo hacker/dashboard para o módulo Metas do Cockpit.

Aparência: terminal old-school, cores verde/amarelo em fundo preto,
box-drawing characters, atualização ao vivo (Live) e menu por teclas.
"""

from __future__ import annotations

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from cockpit.modulos.metas.models import VALID_PRIORITIES
from cockpit.modulos.metas.service import GoalService
from cockpit.modulos.metas.storage import GoalStorage


# Cores estilo terminal hacker
COLOR_OK = "green"
COLOR_PEND = "bright_green"
COLOR_PRIO_ALTA = "bright_red"
COLOR_PRIO_MEDIA = "bright_yellow"
COLOR_PRIO_BAIXA = "bright_cyan"
COLOR_BORDER = "green"


def _status_char(concluida: bool) -> str:
    return "[x]" if concluida else "[ ]"


def _prio_color(prioridade: str) -> str:
    return {
        "alta": COLOR_PRIO_ALTA,
        "media": COLOR_PRIO_MEDIA,
        "baixa": COLOR_PRIO_BAIXA,
    }.get(prioridade, COLOR_PRIO_MEDIA)


class CockpitCLI:
    """Interface de linha de comando estilo dashboard hacker."""

    def __init__(self) -> None:
        self.console = Console()
        self.service = GoalService(GoalStorage("data/metas.db"))
        self.running = True

    # ------------------------------------------------------------------ #
    # Renderização do dashboard
    # ------------------------------------------------------------------ #
    def render(self) -> Panel:
        """Constrói o painel visual completo."""

        linhas: list[str] = []
        resumo = self.service.resumo()
        metas = self.service.listar_metas()

        # Cabeçalho
        linhas.append("═════════════════════════════════════════════════════════════════════")
        linhas.append("                    COCKPIT PESSOAL — MÓDULO METAS")
        linhas.append("═════════════════════════════════════════════════════════════════════")
        linhas.append("")

        # Resumo
        linhas.append(
            f"  Total: {resumo['total']}   |   "
            f"Pendentes: {resumo['pendentes']}   |   "
            f"Concluídas: {resumo['concluidas']}"
        )
        linhas.append("")
        linhas.append("  M E T A S")
        linhas.append("  ───────────────────────────────────────────────────────────────")

        if not metas:
            linhas.append("  (nenhuma meta cadastrada)")
        else:
            for meta in metas:
                status = _status_char(meta.concluida)
                prio = meta.prioridade
                prazo = f"  prazo: {meta.prazo}" if meta.prazo else ""
                linha = f"  {status}  #{meta.id:03d}  {meta.titulo}   [{prio}]{prazo}"
                linhas.append(linha)

        linhas.append("")
        linhas.append("════════════════════════════════════════════════════════════════════")
        linhas.append("  AÇÕES:")
        linhas.append("  [1] Criar nova meta")
        linhas.append("  [2] Marcar como concluída")
        linhas.append("  [3] Reabrir meta")
        linhas.append("  [4] Deletar meta")
        linhas.append("  [5] Atualizar tela")
        linhas.append("  [0] Sair")
        linhas.append("════════════════════════════════════════════════════════════════════")
        linhas.append("")
        linhas.append("  Digite a opção e pressione Enter:")

        texto = "\n".join(linhas)
        return Panel(
            Text(texto, style="green"),
            border_style="green",
            title="[bright_green]COCKPIT[/bright_green]",
            title_align="left",
        )

    # ------------------------------------------------------------------ #
    # Loop principal
    # ------------------------------------------------------------------ #
    def executar(self) -> None:
        self.console.clear()
        with Live(self.render(), console=self.console, refresh_per_second=4) as live:
            while self.running:
                live.update(self.render())
                # Para o Live antes de ler input (evita conflito no terminal)
                live.stop()
                try:
                    opcao = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    self.running = False
                    live.start()
                    break

                if opcao == "0":
                    self.running = False
                    live.start()
                    break
                elif opcao == "1":
                    self._criar_meta(live)
                elif opcao == "2":
                    self._alterar_status(live, concluir=True)
                elif opcao == "3":
                    self._alterar_status(live, concluir=False)
                elif opcao == "4":
                    self._deletar_meta(live)
                elif opcao == "5":
                    pass  # apenas atualiza o loop
                else:
                    self._mensagem(live, "Opção inválida. Tente novamente.")
                live.start()

        self.console.print("[green]Encerrando Cockpit...[/green]")

    # ------------------------------------------------------------------ #
    # Ações
    # ------------------------------------------------------------------ #
    def _criar_meta(self, live: Live) -> None:
        live.stop()
        self.console.print("\n[bright_green]--- NOVA META ---[/bright_green]")
        titulo = input("Título: ").strip()
        if not titulo:
            self._mensagem(live, "Título é obrigatório.")
            return
        descricao = input("Descrição (opcional): ").strip()
        prazo = input("Prazo (YYYY-MM-DD, opcional): ").strip() or None
        print("Prioridades: baixa, media, alta")
        prioridade = input("Prioridade [media]: ").strip() or "media"

        try:
            self.service.criar_meta(
                titulo=titulo,
                descricao=descricao,
                prazo=prazo,
                prioridade=prioridade,
            )
        except ValueError as exc:
            self._mensagem(live, str(exc))
            return

        self._mensagem(live, "Meta criada com sucesso!")

    def _alterar_status(self, live: Live, concluir: bool) -> None:
        live.stop()
        acao = "CONCLUIR" if concluir else "REABRIR"
        self.console.print(f"\n[bright_green]--- {acao} META ---[/bright_green]")
        try:
            goal_id = int(input("ID da meta: ").strip())
        except ValueError:
            self._mensagem(live, "ID inválido.")
            return

        if concluir:
            resultado = self.service.concluir_meta(goal_id)
        else:
            resultado = self.service.reabrir_meta(goal_id)

        if resultado is None:
            self._mensagem(live, "Meta não encontrada.")
        else:
            status_txt = "concluída" if concluir else "reaberta"
            self._mensagem(live, f"Meta #{goal_id} {status_txt}!")

    def _deletar_meta(self, live: Live) -> None:
        live.stop()
        self.console.print("\n[bright_red]--- DELETAR META ---[/bright_red]")
        try:
            goal_id = int(input("ID da meta: ").strip())
        except ValueError:
            self._mensagem(live, "ID inválido.")
            return

        confirmacao = input(f"Confirma deletar a meta #{goal_id}? (s/N): ").strip().lower()
        if confirmacao != "s":
            self._mensagem(live, "Operação cancelada.")
            return

        if self.service.deletar_meta(goal_id):
            self._mensagem(live, f"Meta #{goal_id} deletada.")
        else:
            self._mensagem(live, "Meta não encontrada.")

    def _mensagem(self, live: Live, texto: str) -> None:
        self.console.print(f"\n[bright_yellow]>{texto}[/bright_yellow]")
        input("\nPressione Enter para continuar...")
        live.start()


def main() -> None:
    app = CockpitCLI()
    app.executar()


if __name__ == "__main__":
    main()