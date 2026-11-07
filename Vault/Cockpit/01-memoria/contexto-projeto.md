---
tags: [memoria, contexto, cockpit]
created: 2026-11-07
status: ativo
---

# Contexto do Projeto — Cockpit

## O que é
Cockpit pessoal em Python para concentrar detalhes da vida: agenda, metas, wishlist, emails e mais. É um portfólio público no GitHub.

## Por que existe
Pedro (Brasil, UTC-03) quer um único lugar para monitorar sua vida, construindo um portfólio de projeto com git versionado e documentação conectada no Obsidian.

## Princípios
- **Dados do Cockpit** vivem em SQL/JSON (local, fora do vault).
- **Documentação do projeto** vive em `.md` no vault do Obsidian (duas coisas distintas).
- **Obsidian é só para desenvolvimento**: criar notas de contexto, decisões e planejamento. Não é usado pelo Cockpit em tempo de execução.
- **Primeiro módulo**: Metas. Define o padrão de desenvolvimento aos demais.
- **Interface**: TUI limpa.
- **Segurança**: senhas/tokens em `.env`, nunca commiteados.
- **Código funcional primeiro**: testes automatizados vêm depois.

## Módulos planejados
1. [[03-modulos/metas|Metas]] (MVP, em andamento)
2. Agenda (Google Calendar + input manual)
3. Wishlist
4. Emails (Gmail, enviar e receber)

## Stack
Python 3.14.9, pip + requirements.txt, TUI (Textual), SQL/JSON para dados, Git + GitHub público.

---
> Fonte: conversa com Hermes Agent, 07/11/2026.