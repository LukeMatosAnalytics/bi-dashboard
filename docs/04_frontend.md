# Frontend — Documentação Técnica

Este documento descreve a estrutura, padrões e decisões adotadas
no frontend da plataforma BI Dashboard Web.

---

## Tecnologias Utilizadas

- Framework: React
- Linguagem: JavaScript / TypeScript
- Estilização: CSS utilitário (Tailwind ou similar)
- Gráficos: ApexCharts / Recharts
- Autenticação: Microsoft (MSAL)

---

## Estrutura de Pastas

A estrutura do frontend seguirá o padrão abaixo:

frontend/
├─ src/
│  ├─ pages/
│  │  ├─ DashboardOperacional.jsx
│  │  └─ DashboardGerencial.jsx
│  ├─ components/
│  │  ├─ charts/
│  │  ├─ layout/
│  │  └─ ui/
│  ├─ services/
│  │  └─ api.js
│  ├─ hooks/
│  │  ├─ useAuth.js
│  │  ├─ useDashboardData.js
│  │  └─ useAutoRefresh.js
│  ├─ layouts/
│  │  └─ MainLayout.jsx
│  └─ utils/
│     └─ formatters.js
├─ public/
└─ README.md

---

## Organização de Componentes

- Pages: representam telas completas
- Components: componentes reutilizáveis
- Charts: gráficos específicos
- Layout: estrutura visual (header, sidebar)
- Hooks: lógica reutilizável
- Services: comunicação com API

---

## Consumo da API

- Todas as requisições passam pelo serviço `api.js`
- O frontend nunca monta SQL
- Tokens são enviados via header Authorization
- Tratamento centralizado de erros

---

## Atualização de Dados

- Dados carregados ao abrir a tela
- Atualização automática a cada 30 minutos
- Botão de atualização manual
- Indicador de última atualização visível

---

## Filtros e Interações

- Filtros aplicados no frontend
- Parâmetros enviados à API
- Mudança de filtros dispara nova requisição
- Estado dos filtros mantido na tela

---

## Boas Práticas

- Componentes pequenos e reutilizáveis
- Separação clara de responsabilidades
- Evitar lógica de negócio complexa no frontend
- Padronização visual
- Código legível e documentado

---

## Objetivos do Frontend

- Visual limpo e moderno
- Experiência intuitiva
- Facilidade de manutenção
- Performance adequada
