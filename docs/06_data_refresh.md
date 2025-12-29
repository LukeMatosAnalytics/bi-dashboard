# Atualização de Dados — Regras e Funcionamento

Este documento descreve como funciona o processo de atualização
de dados da plataforma BI Dashboard Web.

---

## Tipos de Atualização

### Atualização Automática
- Executada automaticamente pelo sistema
- Intervalo padrão: 30 minutos
- Ocorre apenas enquanto a tela estiver ativa
- Utiliza cache controlado pelo backend

---

### Atualização Manual
- Disparada pelo usuário
- Ignora o cache existente
- Atualiza os dados imediatamente
- Atualiza o cache após execução

---

## Controle de Cache

- O cache é gerenciado exclusivamente pelo backend
- Cada conjunto de dados possui uma chave de cache
- TTL padrão: 30 minutos
- Cache identificado por endpoint + filtros

---

## Fluxo de Atualização Automática

1. Frontend solicita dados
2. Backend verifica cache
3. Cache válido → retorna dados
4. Cache expirado → consulta banco
5. Atualiza cache
6. Retorna dados ao frontend

---

## Fluxo de Atualização Manual

1. Usuário clica em "Atualizar agora"
2. Frontend envia requisição com parâmetro `force=true`
3. Backend ignora cache
4. Backend consulta banco
5. Atualiza cache
6. Retorna dados ao frontend

---

## Indicadores de Atualização

- Exibição da data e hora da última atualização
- Indicação visual durante atualização
- Mensagens de erro amigáveis em caso de falha

---

## Boas Práticas

- Evitar atualizações muito frequentes
- Centralizar lógica de cache no backend
- Evitar consultas diretas ao banco pelo frontend
- Monitorar impacto no banco de dados

---

## Objetivos da Atualização de Dados

- Garantir dados atualizados
- Minimizar impacto no banco
- Oferecer controle ao usuário
- Manter boa experiência
