---
tags: [setup, instalacao]
created: 2026-11-07
status: ativo
---

# Instalação e Ambiente

## Pré-requisitos
- Python 3.14.9 (instalado na máquina)
- Git 2.53.0

## Passos
1. Clone o repositório (quando criado no GitHub):
   ```bash
   git clone https://github.com/<usuario>/Cockpit.git
   cd Cockpit
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Copie o exemplo de secrets:
   ```bash
   copy .env.example .env
   ```
   Edite `.env` com suas credenciais (nunca commitear).

## Execução
```bash
python -m cockpit
```

## Vault do Obsidian
Abra a pasta `Vault/Cockpit` no Obsidian para ler a documentação conectada do projeto.

---
> Ambiente configurado para o projeto Cockpit.