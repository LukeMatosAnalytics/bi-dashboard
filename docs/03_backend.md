# Backend — Documentação Técnica

Este documento descreve a organização, responsabilidades e padrões
adotados no backend da plataforma BI Dashboard Web.

---

## Tecnologias Utilizadas

- Linguagem: Python
- Framework: FastAPI
- Autenticação: Token JWT (Microsoft)
- Cache: Memória / Redis (futuro)
- Acesso a dados: SQL via driver apropriado

---

## Estrutura de Pastas

A estrutura do backend seguirá o padrão abaixo:

backend/
├─ app/
│  ├─ main.py
│  ├─ routers/
│  │  └─ dashboard.py
│  ├─ services/
│  │  └─ dashboard_service.py
│  ├─ repositories/
│  │  └─ dashboard_repository.py
│  ├─ schemas/
│  │  └─ dashboard_schema.py
│  ├─ core/
│  │  ├─ auth.py
│  │  ├─ cache.py
│  │  └─ config.py
│  └─ utils/
│     └─ logger.py
├─ requirements.txt
└─ README.md

---

## Responsabilidade das Camadas

### Router
- Recebe requisições HTTP
- Valida parâmetros
- Dispara chamadas para os serviços
- Não contém regra de negócio

---

### Service
- Contém regras de negócio
- Orquestra chamadas ao banco
- Controla cache
- Aplica filtros e permissões

---

### Repository
- Responsável por acessar o banco de dados
- Contém consultas SQL
- Não possui lógica de negócio

---

### Schemas
- Define contratos de entrada e saída
- Garante consistência dos dados
- Facilita validação e documentação

---

## Padrão de Endpoints

Exemplo de endpoint:

GET /api/dashboard/sprints

Parâmetros comuns:
- inicio (data)
- fim (data)
- filtros adicionais
- force (boolean)

Exemplo:
GET /api/dashboard/sprints?inicio=2025-01-01&fim=2025-01-31&force=true

---

## Autenticação e Segurança

- O backend valida o token JWT recebido do frontend
- O token é emitido pelo Microsoft Entra ID
- Nenhuma senha é armazenada
- O acesso ao banco é feito com usuário técnico

---

## Cache de Dados

- Cache controlado pelo backend
- TTL padrão: 30 minutos
- Atualização manual ignora cache
- Cache identificado por endpoint + filtros

---

## Conexão com Banco de Dados

- A conexão utiliza credenciais técnicas
- Credenciais armazenadas de forma segura
- Uso preferencial de views analíticas
- Consultas otimizadas para leitura

---

## Logs e Monitoramento

- Registro de erros
- Registro de acessos
- Registro de atualizações manuais
- Logs preparados para auditoria

---

## Princípios do Backend

- Clareza de responsabilidades
- Código simples e legível
- Facilidade de manutenção
- Segurança por padrão
- Performance previsível
