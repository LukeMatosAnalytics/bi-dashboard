# Arquitetura do Sistema

Este documento descreve a arquitetura da plataforma de BI Dashboard Web,
incluindo seus componentes, responsabilidades e fluxo de dados.

---

## Visão Geral da Arquitetura

A aplicação segue uma arquitetura em camadas, separando claramente
responsabilidades entre frontend, backend e banco de dados.

Componentes principais:
- Frontend Web (visualização e interação)
- Backend API (regra de negócio e acesso a dados)
- Banco de Dados Corporativo (fonte de dados)
- Serviço de Autenticação Microsoft (Azure AD / Entra ID)

---

## Componentes do Sistema

### Frontend
Responsável por:
- Interface visual dos dashboards
- Filtros e interações do usuário
- Exibição de gráficos e indicadores
- Disparo de atualização manual e automática

Tecnologias previstas:
- React
- Bibliotecas de gráficos (ApexCharts / Recharts)
- CSS utilitário (Tailwind ou equivalente)

O frontend **não acessa o banco de dados diretamente**.

---

### Backend (API)
Responsável por:
- Autenticação e validação do usuário
- Aplicação das regras de negócio
- Consulta ao banco de dados
- Cache de dados
- Entrega de dados prontos para visualização

Tecnologias previstas:
- Python
- FastAPI
- Camada de cache (Redis ou memória)

O backend atua como intermediário entre frontend e banco de dados.

---

### Banco de Dados
Responsável por:
- Armazenar dados operacionais e históricos
- Disponibilizar dados por meio de views analíticas
- Garantir integridade e performance

Boas práticas adotadas:
- Uso de views para consumo analítico
- Evitar consultas diretas a tabelas transacionais
- Centralização das regras de cálculo no banco quando possível

---

### Autenticação (Microsoft)
Responsável por:
- Autenticar usuários via login corporativo
- Fornecer token de identidade (JWT)
- Permitir controle de acesso por grupos ou perfis

Tecnologia:
- Azure AD / Entra ID
- Login federado (SSO)

O sistema **não armazena senhas de usuários**.

---

## Fluxo de Dados

1. Usuário acessa o frontend
2. Usuário autentica via Microsoft
3. Frontend envia token ao backend
4. Backend valida o token
5. Backend consulta o banco de dados
6. Backend aplica regras e cache
7. Backend retorna dados ao frontend
8. Frontend exibe dashboards e gráficos

---

## Atualização de Dados

- Atualização automática a cada 30 minutos
- Opção de atualização manual pelo usuário
- Cache controlado pelo backend
- Indicador de "última atualização" exibido no frontend

---

## Considerações de Segurança

- Acesso ao banco feito apenas pelo backend
- Credenciais armazenadas em local seguro (Key Vault ou variáveis de ambiente)
- Controle de acesso por usuário e/ou grupo
- Logs de acesso e atualização

---

## Objetivos da Arquitetura

- Clareza de responsabilidades
- Facilidade de manutenção
- Escalabilidade futura
- Segurança corporativa
- Boa experiência do usuário
