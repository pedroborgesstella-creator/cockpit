---
tags: [planejamento, mvp, metas]
created: 2026-11-07
status: em_andamento
---

# MVP — Módulo Metas

## Objetivo
Entregar o primeiro módulo funcional do Cockpit: gerenciamento de metas pessoais, definindo o padrão de desenvolvimento para os próximos módulos.

## Escopo
- Criar meta (título, descrição, prazo, prioridade)
- Listar metas (pendentes, concluídas, todas)
- Marcar meta como concluída / reabrir
- Deletar meta
- Armazenamento em SQLite (arquivo local `data/metas.db`)
- TUI limpa (Textual)

## Fora do escopo (MVP)
- Notificações
- Sincronização em nuvem
- Testes automatizados
- Integração com Obsidian em tempo de execução

## Critérios de aceitação
- [ ] Usuário consegue criar uma meta via TUI
- [ ] Lista de metas exibe título, status e prazo
- [ ] Meta pode ser marcada como concluída
- [ ] Dados persistem entre execuções
- [ ] `.env.example` existe, `.env` não é commiteado

---
> MVP definido com o usuário (foco em metas primeiro, 07/11/2026).