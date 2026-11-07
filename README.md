# Cockpit

Cockpit pessoal em Python para monitorar minha vida: metas, agenda, wishlist, emails e mais.

## Status

Em desenvolvimento — primeiro módulo (Metas) funcional.

## Estrutura

```
Cockpit/
├── cockpit/              # Código fonte (pacote Python)
│   ├── __main__.py       # Ponto de entrada: python -m cockpit
│   ├── modulos/metas/    # Módulo Metas (modelo, armazenamento, serviço)
│   └── ui/app.py         # TUI limpa (Textual)
├── data/                 # Banco SQLite local (não versionado)
├── Vault/                # Documentação no Obsidian (não parte do código)
├── requirements.txt      # Dependências
├── .env.example          # Exemplo de variáveis secretas
└── .gitignore
```

## Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/Cockpit.git
cd Cockpit

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure as variáveis secretas (quando necessário)
copy .env.example .env

# 5. Execute
python -m cockpit
```

## Módulo Metas (MVP)

- Criar meta (título, descrição, prazo, prioridade)
- Listar metas (todas, pendentes, concluídas)
- Marcar como concluída / reabrir
- Deletar meta
- Armazenamento local em SQLite (`data/metas.db`)

## Documentação

O projeto é documentado dentro do vault do Obsidian (`Vault/Cockpit/`), com notas conectadas sobre contexto, decisões de arquitetura, tecnologias, planejamento e roadmap.

## Segredo

Variáveis sensíveis (Gmail, Google Calendar) ficam em `.env`, que está no `.gitignore` e nunca será commiteado.

## Licença

Livre para portfólio pessoal.