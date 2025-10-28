# Casos de Teste - Filtros Rápidos de Data

## Objetivo

Validar que os filtros rápidos de data estão funcionando corretamente na `TransactionListView`.

---

## Pré-requisitos

1. Usuário logado no sistema
2. Pelo menos 3 contas criadas
3. Pelo menos 5 categorias criadas
4. Transações distribuídas em diferentes períodos:
   - Transações do mês atual
   - Transações do mês passado
   - Transações de meses anteriores
   - Transações do ano atual
   - Transações de anos anteriores

---

## Caso de Teste 1: Filtro "Este Mês"

**Objetivo:** Validar que apenas transações do mês atual são exibidas.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=this_month` à URL (ou clique no botão correspondente)
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações com data entre o primeiro dia do mês atual e hoje são exibidas
- ✅ A variável `active_quick_filter` no contexto tem valor `'this_month'`
- ✅ O botão/link "Este Mês" está destacado visualmente
- ✅ Estatísticas (receitas, despesas, saldo) refletem apenas as transações filtradas

**Exemplo:**
- Hoje: 2025-10-28
- Data Início: 2025-10-01
- Data Fim: 2025-10-28

---

## Caso de Teste 2: Filtro "Último Mês"

**Objetivo:** Validar que apenas transações do mês anterior completo são exibidas.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=last_month` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações do mês anterior (do primeiro ao último dia) são exibidas
- ✅ `active_quick_filter` = `'last_month'`
- ✅ Botão destacado corretamente

**Exemplo:**
- Hoje: 2025-10-28
- Data Início: 2025-09-01
- Data Fim: 2025-09-30

---

## Caso de Teste 3: Filtro "Este Ano"

**Objetivo:** Validar que apenas transações do ano atual são exibidas.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=this_year` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações de 1º de janeiro do ano atual até hoje são exibidas
- ✅ `active_quick_filter` = `'this_year'`
- ✅ Transações de anos anteriores NÃO aparecem

**Exemplo:**
- Hoje: 2025-10-28
- Data Início: 2025-01-01
- Data Fim: 2025-10-28

---

## Caso de Teste 4: Filtro "Últimos 30 Dias"

**Objetivo:** Validar que apenas transações dos últimos 30 dias são exibidas.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=last_30_days` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações dos últimos 30 dias (incluindo hoje) são exibidas
- ✅ `active_quick_filter` = `'last_30_days'`
- ✅ Transações mais antigas que 30 dias NÃO aparecem

**Exemplo:**
- Hoje: 2025-10-28
- Data Início: 2025-09-28
- Data Fim: 2025-10-28

---

## Caso de Teste 5: Filtro "Últimos 90 Dias"

**Objetivo:** Validar que apenas transações dos últimos 90 dias são exibidas.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=last_90_days` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações dos últimos 90 dias (incluindo hoje) são exibidas
- ✅ `active_quick_filter` = `'last_90_days'`
- ✅ Período cobre aproximadamente 3 meses

**Exemplo:**
- Hoje: 2025-10-28
- Data Início: 2025-07-30
- Data Fim: 2025-10-28

---

## Caso de Teste 6: Prioridade do Filtro Rápido

**Objetivo:** Validar que o filtro rápido tem prioridade sobre os campos manuais.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=this_month&data_inicio=2020-01-01&data_fim=2020-12-31` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações do mês atual são exibidas (filtro rápido tem prioridade)
- ✅ Os campos `data_inicio` e `data_fim` são IGNORADOS
- ✅ `active_quick_filter` = `'this_month'`

---

## Caso de Teste 7: Filtro Manual (Sem Filtro Rápido)

**Objetivo:** Validar que os filtros manuais funcionam quando NÃO há filtro rápido.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?data_inicio=2025-01-01&data_fim=2025-03-31` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações entre 2025-01-01 e 2025-03-31 são exibidas
- ✅ `active_quick_filter` = `None`
- ✅ Nenhum botão de filtro rápido está destacado

---

## Caso de Teste 8: Combinação com Filtro de Conta

**Objetivo:** Validar que filtro rápido funciona junto com filtro de conta.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=this_month&conta=1` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações do mês atual E da conta ID=1 são exibidas
- ✅ `active_quick_filter` = `'this_month'`
- ✅ Filtro de conta permanece selecionado no formulário

---

## Caso de Teste 9: Combinação com Filtro de Categoria

**Objetivo:** Validar que filtro rápido funciona junto com filtro de categoria.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=last_30_days&categoria=5` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações dos últimos 30 dias E da categoria ID=5 são exibidas
- ✅ `active_quick_filter` = `'last_30_days'`
- ✅ Filtro de categoria permanece selecionado no formulário

---

## Caso de Teste 10: Combinação com Busca por Descrição

**Objetivo:** Validar que filtro rápido funciona junto com busca.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=this_year&search=mercado` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Apenas transações do ano atual E com "mercado" na descrição são exibidas
- ✅ `active_quick_filter` = `'this_year'`
- ✅ Campo de busca permanece preenchido com "mercado"

---

## Caso de Teste 11: Combinação com Múltiplos Filtros

**Objetivo:** Validar que filtro rápido funciona com múltiplos filtros simultaneamente.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=last_90_days&conta=1&categoria=3&search=netflix` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Transações devem atender TODOS os critérios:
  - Últimos 90 dias
  - Conta ID=1
  - Categoria ID=3
  - Descrição contém "netflix"
- ✅ `active_quick_filter` = `'last_90_days'`
- ✅ Todos os filtros permanecem selecionados

---

## Caso de Teste 12: Filtro Inválido

**Objetivo:** Validar comportamento quando filtro rápido inválido é fornecido.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?period=invalid_period` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ TODAS as transações do usuário são exibidas (filtro inválido é ignorado)
- ✅ `active_quick_filter` = `'invalid_period'` (mas sem efeito nos filtros)
- ✅ Nenhum erro é lançado

---

## Caso de Teste 13: Limpar Filtro Rápido

**Objetivo:** Validar que é possível remover o filtro rápido.

**Passos:**
1. Acesse `/transacoes/?period=this_month`
2. Remova o parâmetro `period` da URL (acesse apenas `/transacoes/`)
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ TODAS as transações do usuário são exibidas
- ✅ `active_quick_filter` = `None`
- ✅ Nenhum botão está destacado

---

## Caso de Teste 14: Parâmetro Alternativo `quick_filter`

**Objetivo:** Validar que `quick_filter` funciona como alternativa a `period`.

**Passos:**
1. Acesse `/transacoes/`
2. Adicione `?quick_filter=this_month` à URL
3. Observe as transações exibidas

**Resultado Esperado:**
- ✅ Comportamento idêntico a `?period=this_month`
- ✅ `active_quick_filter` = `'this_month'`

---

## Caso de Teste 15: Estatísticas Corretas

**Objetivo:** Validar que estatísticas refletem apenas transações filtradas.

**Passos:**
1. Acesse `/transacoes/?period=this_month`
2. Observe os valores de:
   - Total de receitas
   - Total de despesas
   - Saldo

**Resultado Esperado:**
- ✅ Total de receitas = soma de transações do tipo "income" DO MÊS ATUAL
- ✅ Total de despesas = soma de transações do tipo "expense" DO MÊS ATUAL
- ✅ Saldo = receitas - despesas (ambas do mês atual)
- ✅ Valores NÃO incluem transações de outros períodos

---

## Caso de Teste 16: Paginação com Filtro

**Objetivo:** Validar que paginação funciona corretamente com filtro rápido.

**Passos:**
1. Acesse `/transacoes/?period=this_year`
2. Se houver mais de 20 transações, navegue para a página 2
3. Observe que o filtro permanece ativo

**Resultado Esperado:**
- ✅ Filtro permanece ativo na página 2
- ✅ URL contém `?period=this_year&page=2`
- ✅ Apenas transações do ano atual são exibidas na página 2

---

## Caso de Teste 17: Ordenação com Filtro

**Objetivo:** Validar que ordenação funciona com filtro rápido.

**Passos:**
1. Acesse `/transacoes/?period=last_30_days`
2. Clique para ordenar por valor (amount)
3. Observe que o filtro permanece ativo

**Resultado Esperado:**
- ✅ Transações são ordenadas por valor
- ✅ Filtro rápido permanece ativo
- ✅ URL contém `?period=last_30_days&sort=amount&direction=asc`

---

## Caso de Teste 18: Mudança de Filtro Rápido

**Objetivo:** Validar que é possível trocar entre diferentes filtros rápidos.

**Passos:**
1. Acesse `/transacoes/?period=this_month`
2. Altere para `?period=last_month`
3. Altere para `?period=this_year`
4. Observe as mudanças nas transações exibidas

**Resultado Esperado:**
- ✅ Cada mudança exibe o conjunto correto de transações
- ✅ `active_quick_filter` é atualizado corretamente em cada mudança
- ✅ Estatísticas são recalculadas para cada filtro

---

## Checklist de Validação Final

- [ ] Todos os 5 filtros rápidos funcionam corretamente
- [ ] Prioridade sobre filtros manuais está implementada
- [ ] `active_quick_filter` é adicionado ao contexto
- [ ] Filtros rápidos funcionam com outros filtros (conta, categoria, busca)
- [ ] Estatísticas refletem apenas transações filtradas
- [ ] Paginação funciona com filtros rápidos
- [ ] Ordenação funciona com filtros rápidos
- [ ] Nenhum erro é lançado com filtros inválidos
- [ ] É possível limpar/remover o filtro rápido
- [ ] Parâmetros `period` e `quick_filter` funcionam

---

## Notas para QA Tester

1. **Data do servidor:** Os testes assumem que a data do servidor está correta. Verifique `datetime.now().date()` no Django shell se necessário.

2. **Fuso horário:** Em produção, considere usar `timezone.now()` para garantir consistência.

3. **Criação de dados de teste:** Use o Django shell para criar transações em diferentes períodos:

```python
from transactions.models import Transaction
from accounts.models import Account
from categories.models import Category
from datetime import datetime, timedelta

# Transação de hoje
Transaction.objects.create(...)

# Transação de 35 dias atrás
Transaction.objects.create(
    transaction_date=datetime.now().date() - timedelta(days=35),
    ...
)

# Transação do ano passado
Transaction.objects.create(
    transaction_date=datetime(2024, 1, 15).date(),
    ...
)
```

4. **Isolamento de dados:** Cada usuário vê apenas suas próprias transações. Teste com múltiplos usuários para validar isolamento.
