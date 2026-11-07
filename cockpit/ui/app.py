"""TUI limpa para o módulo Metas usando Textual."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label, Select, Static
from textual.reactive import reactive

from cockpit.modulos.metas.models import Goal, VALID_PRIORITIES
from cockpit.modulos.metas.service import GoalService
from cockpit.modulos.metas.storage import GoalStorage


class MetaCard(Static):
    """Card simples exibindo uma meta."""

    def __init__(self, goal: Goal, **kwargs) -> None:
        super().__init__(**kwargs)
        self.goal = goal
        self.update(self._render())

    def _render(self) -> str:
        status = "✓" if self.goal.concluida else "○"
        prazo = f" | prazo: {self.goal.prazo}" if self.goal.prazo else ""
        return f"{status} #{self.goal.id}  {self.goal.titulo}  [prioridade: {self.goal.prioridade}]{prazo}"

    def refresh_view(self) -> None:
        self.update(self._render())


class NovaMetaModal(Static):
    """Formulário simples para criar uma nova meta."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Label("Nova meta")
        yield Input(placeholder="Título da meta", id="input_titulo")
        yield Input(placeholder="Descrição (opcional)", id="input_descricao")
        yield Input(placeholder="Prazo (YYYY-MM-DD, opcional)", id="input_prazo")
        yield Select(
            options=[(p.title(), p) for p in sorted(VALID_PRIORITIES)],
            value="media",
            id="select_prioridade",
        )
        yield Button("Criar", id="btn_criar_meta", variant="primary")
        yield Button("Cancelar", id="btn_cancelar_meta")


class CockpitApp(App):
    """Aplicação principal do Cockpit — TUI limpa."""

    CSS = """
    Screen {
        align: center middle;
    }
    #principal {
        width: 80;
        height: auto;
        border: solid $accent;
        padding: 1 2;
    }
    #lista_metas {
        height: 20;
        overflow-y: auto;
        border: solid $surface;
        padding: 1;
    }
    Horizontal {
        height: auto;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        service = GoalService(GoalStorage("data/metas.db"))
        self.service = service
        self._modal_aberto = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Cockpit — Metas", id="titulo_tela"),
            Static(id="resumo"),
            VerticalScroll(id="lista_metas"),
            Horizontal(
                Button("Adicionar meta", id="btn_adicionar", variant="primary"),
                Button("Atualizar lista", id="btn_atualizar"),
                Button("Sair", id="btn_sair", variant="error"),
            ),
            id="principal",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.atualizar_lista()

    def atualizar_lista(self) -> None:
        resumo = self.service.resumo()
        resumo_text = (
            f"Total: {resumo['total']}  |  "
            f"Pendentes: {resumo['pendentes']}  |  "
            f"Concluídas: {resumo['concluidas']}"
        )
        self.query_one("#resumo", Static).update(resumo_text)

        lista = self.query_one("#lista_metas", VerticalScroll)
        lista.remove_children()
        for meta in self.service.listar_metas():
            lista.mount(MetaCard(meta))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        botao_id = event.button.id
        if botao_id == "btn_adicionar":
            self.abrir_modal_nova_meta()
        elif botao_id == "btn_atualizar":
            self.atualizar_lista()
        elif botao_id == "btn_sair":
            self.exit()
        elif botao_id == "btn_criar_meta":
            self.criar_meta_do_modal()
        elif botao_id == "btn_cancelar_meta":
            self.fechar_modal()

    def abrir_modal_nova_meta(self) -> None:
        if self._modal_aberto:
            return
        self._modal_aberto = True
        self.mount(NovaMetaModal(id="modal_nova_meta"))

    def fechar_modal(self) -> None:
        try:
            self.query_one("#modal_nova_meta").remove()
        except Exception:
            pass
        self._modal_aberto = False

    def criar_meta_do_modal(self) -> None:
        try:
            titulo = self.query_one("#input_titulo", Input).value
            descricao = self.query_one("#input_descricao", Input).value
            prazo = self.query_one("#input_prazo", Input).value or None
            prioridade = self.query_one("#select_prioridade", Select).value
            if prioridade == Select.BLANK:
                prioridade = "media"
            self.service.criar_meta(titulo=titulo, descricao=descricao, prazo=prazo, prioridade=prioridade)
        except ValueError as exc:
            self.notify(str(exc), severity="error", timeout=3)
            return
        self.fechar_modal()
        self.atualizar_lista()
        self.notify("Meta criada com sucesso!", severity="information", timeout=2)