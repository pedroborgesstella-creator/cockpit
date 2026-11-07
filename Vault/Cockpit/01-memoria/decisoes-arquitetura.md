---
tags: [memoria, decisao, arquitetura]
created: 2026-11-07
status: aprovada
---

# Decisões de Arquitetura — Cockpit

## Separação de responsabilidades
- **Camada de dados**: SQL/JSON local. Cada módulo tem seu próprio repositório de dados (ex: `data/metas.db` ou `data/metas.json`).
- **Camada de negócio**: regras do módulo (ex: criar meta, concluir meta, listar metas pendentes).
- **Camada de apresentação**: TUI limpa (Textual). Sem dependência do Obsidian em tempo de execução.

## Armazenamento
- Dados do usuário: nunca entram no repositório Git (`.gitignore` cobre `data/`, `.env`, `*.db`, `*.json` de dados).
- Documentação: notas `.md` no vault, versionadas separadamente ou no mesmo repositório como referência.

## Padrão de módulo
Cada módulo segue:
```
cockpit/
  modulos/
    <modulo>/
      models.py      # entidades (ex: Goal)
      storage.py     # leitura/gravação (SQL/JSON)
      service.py     # regras de negócio
  cli/
    <modulo>.py      # interface TUI/CLI
```

## Comunicação com serviços externos
- Gmail: SMTP/IMAP via variáveis de ambiente (`GMAIL_USER`, `GMAIL_APP_PASSWORD`).
- Google Calendar: OAuth (futuro), credenciais fora do repositório.

---
> Decisão tomada na definição do MVP (07/11/2026).