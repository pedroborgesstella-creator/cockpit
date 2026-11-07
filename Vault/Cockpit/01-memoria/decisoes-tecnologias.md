---
tags: [memoria, decisao, tecnologias]
created: 2026-11-07
status: aprovada
---

# Decisões de Tecnologias — Cockpit

| Item | Escolha | Justificativa |
|------|---------|---------------|
| Linguagem | Python 3.14.9 | Versão instalada na máquina do usuário |
| Gerenciador de pacotes | pip + requirements.txt | Simplicidade e portfólio |
| Interface | Textual (TUI) | TUI limpa, moderna, terminal-first |
| Dados | SQL (SQLite) + JSON | Simples, sem servidor, fácil backup |
| Versionamento | Git + GitHub (público) | Portfólio, repositório "Cockpit" |
| Documentação | Obsidian (.md, wikilinks) | Cérebro conectado do projeto |
| Secrets | .env + .gitignore | Nunca commitear credenciais |
| Testes | Depois do código funcional | Foco inicial na entrega |

## Dependências iniciais (requirements.txt)
- `textual` — TUI
- (outras a serem adicionadas conforme os módulos)

---
> Decisão tomada na definição do MVP (07/11/2026).