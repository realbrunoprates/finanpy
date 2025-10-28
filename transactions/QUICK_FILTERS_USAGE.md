# Filtros Rápidos de Data - Documentação

## Visão Geral

Os filtros rápidos de data foram implementados na `TransactionListView` para permitir filtragem rápida de transações por períodos comuns sem a necessidade de inserir datas manualmente.

## Parâmetros Aceitos

A view aceita dois parâmetros GET equivalentes:
- `period` (recomendado)
- `quick_filter` (alternativa)

## Períodos Suportados

### 1. Este Mês (`this_month`)
Filtra transações do primeiro dia do mês atual até hoje.

**Exemplo de URL:**
```
/transacoes/?period=this_month
```

**Cálculo:**
- Data Início: Primeiro dia do mês atual
- Data Fim: Hoje

---

### 2. Último Mês (`last_month`)
Filtra transações do mês anterior completo.

**Exemplo de URL:**
```
/transacoes/?period=last_month
```

**Cálculo:**
- Data Início: Primeiro dia do mês passado
- Data Fim: Último dia do mês passado

---

### 3. Este Ano (`this_year`)
Filtra transações do primeiro dia do ano atual até hoje.

**Exemplo de URL:**
```
/transacoes/?period=this_year
```

**Cálculo:**
- Data Início: 1º de janeiro do ano atual
- Data Fim: Hoje

---

### 4. Últimos 30 Dias (`last_30_days`)
Filtra transações dos últimos 30 dias (incluindo hoje).

**Exemplo de URL:**
```
/transacoes/?period=last_30_days
```

**Cálculo:**
- Data Início: Hoje - 30 dias
- Data Fim: Hoje

---

### 5. Últimos 90 Dias (`last_90_days`)
Filtra transações dos últimos 90 dias (incluindo hoje).

**Exemplo de URL:**
```
/transacoes/?period=last_90_days
```

**Cálculo:**
- Data Início: Hoje - 90 dias
- Data Fim: Hoje

---

## Prioridade de Filtros

**IMPORTANTE:** Os filtros rápidos têm **prioridade absoluta** sobre os campos manuais `data_inicio` e `data_fim`.

### Exemplo de Comportamento:

**Cenário 1 - Apenas filtro rápido:**
```
/transacoes/?period=this_month
```
✅ Aplica filtro do mês atual

**Cenário 2 - Filtro rápido + campos manuais:**
```
/transacoes/?period=this_month&data_inicio=2025-01-01&data_fim=2025-12-31
```
✅ Aplica filtro do mês atual (ignora data_inicio e data_fim)

**Cenário 3 - Apenas campos manuais:**
```
/transacoes/?data_inicio=2025-01-01&data_fim=2025-12-31
```
✅ Aplica filtro manual (data_inicio e data_fim)

---

## Combinação com Outros Filtros

Os filtros rápidos funcionam perfeitamente com outros filtros existentes:

**Filtro rápido + busca por descrição:**
```
/transacoes/?period=this_month&search=mercado
```

**Filtro rápido + filtro por conta:**
```
/transacoes/?period=last_30_days&conta=1
```

**Filtro rápido + filtro por categoria:**
```
/transacoes/?period=this_year&categoria=5
```

**Filtro rápido + múltiplos filtros:**
```
/transacoes/?period=last_90_days&conta=1&categoria=5&search=netflix
```

---

## Variável de Contexto no Template

A view disponibiliza a variável `active_quick_filter` no contexto do template para indicar qual filtro rápido está ativo.

**Valores possíveis:**
- `'this_month'`
- `'last_month'`
- `'this_year'`
- `'last_30_days'`
- `'last_90_days'`
- `None` (quando nenhum filtro rápido está ativo)

**Exemplo de uso no template:**
```html
{% if active_quick_filter == 'this_month' %}
    <button class="bg-primary-500 text-white">Este Mês</button>
{% else %}
    <button class="bg-gray-500 text-white">Este Mês</button>
{% endif %}
```

---

## Implementação Técnica

### Cálculo de Datas

O cálculo das datas é feito usando `datetime` e `timedelta` do Python:

```python
from datetime import datetime, timedelta

today = datetime.now().date()

# Este mês
data_inicio = today.replace(day=1)
data_fim = today

# Último mês
first_day_this_month = today.replace(day=1)
last_day_last_month = first_day_this_month - timedelta(days=1)
data_inicio = last_day_last_month.replace(day=1)
data_fim = last_day_last_month

# Este ano
data_inicio = today.replace(month=1, day=1)
data_fim = today

# Últimos 30/90 dias
data_inicio = today - timedelta(days=30)  # ou 90
data_fim = today
```

### Ordem de Execução

1. Verifica se existe `period` ou `quick_filter` nos parâmetros GET
2. Se existir, calcula as datas correspondentes
3. Armazena o filtro ativo em `self.active_quick_filter`
4. Aplica os filtros de data no queryset
5. Se NÃO existir filtro rápido, aplica filtros manuais `data_inicio` e `data_fim`
6. Adiciona `active_quick_filter` ao contexto do template

---

## Exemplos de Uso Frontend

### Botões de Filtro Rápido

```html
<div class="flex gap-2 mb-4">
    <a href="?period=this_month"
       class="px-4 py-2 rounded-lg {% if active_quick_filter == 'this_month' %}bg-primary-500 text-white{% else %}bg-gray-200{% endif %}">
        Este Mês
    </a>
    <a href="?period=last_month"
       class="px-4 py-2 rounded-lg {% if active_quick_filter == 'last_month' %}bg-primary-500 text-white{% else %}bg-gray-200{% endif %}">
        Último Mês
    </a>
    <a href="?period=this_year"
       class="px-4 py-2 rounded-lg {% if active_quick_filter == 'this_year' %}bg-primary-500 text-white{% else %}bg-gray-200{% endif %}">
        Este Ano
    </a>
    <a href="?period=last_30_days"
       class="px-4 py-2 rounded-lg {% if active_quick_filter == 'last_30_days' %}bg-primary-500 text-white{% else %}bg-gray-200{% endif %}">
        Últimos 30 dias
    </a>
    <a href="?period=last_90_days"
       class="px-4 py-2 rounded-lg {% if active_quick_filter == 'last_90_days' %}bg-primary-500 text-white{% else %}bg-gray-200{% endif %}">
        Últimos 90 dias
    </a>
</div>
```

### Dropdown de Filtro Rápido

```html
<select name="period" onchange="this.form.submit()"
        class="px-4 py-2 border rounded-lg">
    <option value="">Selecione um período</option>
    <option value="this_month" {% if active_quick_filter == 'this_month' %}selected{% endif %}>
        Este Mês
    </option>
    <option value="last_month" {% if active_quick_filter == 'last_month' %}selected{% endif %}>
        Último Mês
    </option>
    <option value="this_year" {% if active_quick_filter == 'this_year' %}selected{% endif %}>
        Este Ano
    </option>
    <option value="last_30_days" {% if active_quick_filter == 'last_30_days' %}selected{% endif %}>
        Últimos 30 dias
    </option>
    <option value="last_90_days" {% if active_quick_filter == 'last_90_days' %}selected{% endif %}>
        Últimos 90 dias
    </option>
</select>
```

---

## Testes Manuais

Para testar os filtros rápidos:

1. Acesse `/transacoes/`
2. Adicione `?period=this_month` à URL
3. Verifique se apenas transações do mês atual são exibidas
4. Teste cada um dos períodos disponíveis
5. Combine com outros filtros (conta, categoria, busca)
6. Teste a prioridade: adicione `&data_inicio=2020-01-01` com um filtro rápido ativo

---

## Notas Importantes

1. **Timezone:** O cálculo usa `datetime.now().date()`, que retorna a data do servidor. Em produção com PostgreSQL, considere usar `timezone.now()` do Django para consistência.

2. **Performance:** Os filtros rápidos não afetam a performance, pois utilizam índices de data existentes no banco de dados.

3. **Manutenibilidade:** Novos períodos podem ser facilmente adicionados seguindo o mesmo padrão no método `get_queryset()`.

4. **Segurança:** Não há riscos de segurança, pois os valores são comparados com strings hardcoded e as datas são calculadas internamente.

---

## Frontend Developer Next Steps

O Frontend Developer deve implementar a UI para os filtros rápidos no template `transactions/transaction_list.html`:

1. Adicionar botões ou dropdown com os 5 períodos disponíveis
2. Destacar visualmente o filtro ativo usando `active_quick_filter`
3. Permitir limpar o filtro rápido (remover parâmetro `period` da URL)
4. Considerar adicionar ícones ou badges para melhor UX
5. Garantir que o design seja responsivo em mobile

**Referência de design:** Seguir o design system em `docs/design-system.md`
