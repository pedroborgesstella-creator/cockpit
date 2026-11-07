---
tags: [modulo, metas]
created: 2026-11-07
status: em_andamento
---

# Módulo Metas

## Entidade Goal
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | inteiro | sim (auto) | Identificador único |
| titulo | texto | sim | Título da meta |
| descricao | texto | não | Descrição detalhada |
| prazo | data | não | Data limite |
| prioridade | texto | não | baixa, media, alta |
| concluida | booleano | não (padrão: false) | Status de conclusão |
| criado_em | datetime | sim (auto) | Data de criação |

## Regras de negócio
- Título é obrigatório e não pode estar vazio.
- Prioridade aceita apenas: baixa, media, alta.
- Uma meta concluída pode ser reaberta.
- Deleção é permanente (sem lixeira no MVP).

## Armazenamento
- Arquivo: `data/metas.db` (SQLite)
- Nunca commitear `data/` no Git.

## Interface (TUI)
- Tela principal: lista de metas com filtro por status.
- Modal ou tela para criar/editar meta.
- Confirmação antes de deletar.

---
> Especificação do módulo Metas, primeiro módulo do Cockpit.