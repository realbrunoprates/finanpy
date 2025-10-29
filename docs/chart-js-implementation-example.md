# Chart.js Implementation Example

Este documento fornece exemplos de como usar os dados preparados no `DashboardView` para criar gráficos com Chart.js.

## Dados Disponíveis no Context

O `DashboardView` em `core/views.py` agora fornece dois objetos de dados prontos para Chart.js:

### 1. `chart_categories_data` - Gráfico de Pizza (Gastos por Categoria)

Estrutura de dados:
```python
{
    'labels': ['Alimentação', 'Transporte', 'Lazer'],  # Nomes das categorias
    'values': [450.50, 200.00, 150.75],                # Valores totais gastos
    'colors': ['#667eea', '#10b981', '#ef4444']        # Cores das categorias
}
```

**Exemplo de uso no template:**
```html
<script>
    // Dados passados pelo Django
    const categoriesData = {
        labels: {{ chart_categories_data.labels|safe }},
        values: {{ chart_categories_data.values|safe }},
        colors: {{ chart_categories_data.colors|safe }}
    };

    // Criar gráfico de pizza
    const ctx = document.getElementById('categoryPieChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categoriesData.labels,
            datasets: [{
                data: categoriesData.values,
                backgroundColor: categoriesData.colors,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
</script>
```

### 2. `chart_monthly_data` - Gráfico de Linha (Evolução Mensal)

Estrutura de dados:
```python
{
    'labels': ['Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],  # Últimos 6 meses
    'income': [2500.00, 3000.00, 2800.00, 3200.00, 2900.00, 3100.00],
    'expenses': [1800.00, 2200.00, 1900.00, 2400.00, 2100.00, 2300.00]
}
```

**Exemplo de uso no template:**
```html
<script>
    // Dados passados pelo Django
    const monthlyData = {
        labels: {{ chart_monthly_data.labels|safe }},
        income: {{ chart_monthly_data.income|safe }},
        expenses: {{ chart_monthly_data.expenses|safe }}
    };

    // Criar gráfico de linha
    const ctx = document.getElementById('monthlyLineChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: monthlyData.labels,
            datasets: [
                {
                    label: 'Entradas',
                    data: monthlyData.income,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Saídas',
                    data: monthlyData.expenses,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
</script>
```

## Características dos Dados

### Gráfico de Pizza (chart_categories_data)
- Filtra apenas transações do tipo **EXPENSE** (despesas)
- Mostra dados do **mês atual**
- Apenas categorias que tiveram transações aparecem
- Cores são as mesmas definidas para cada categoria no sistema
- Se não houver despesas no mês, as listas estarão vazias

### Gráfico de Linha (chart_monthly_data)
- Mostra os **últimos 6 meses completos**
- Inclui tanto **INCOME** (entradas) quanto **EXPENSE** (saídas)
- Nomes dos meses em **português** abreviado (Jan, Fev, Mar, etc.)
- Se não houver transações em um mês, o valor será 0.0
- Útil para visualizar tendências e comparar entradas vs saídas

## Filtro de Segurança

Ambos os dados são filtrados por `account__user=request.user`, garantindo que:
- Cada usuário vê apenas seus próprios dados
- Não há risco de vazamento de informações entre usuários
- Os dados respeitam a arquitetura de isolamento do Finanpy

## Formato JSON-Ready

Os valores são convertidos para `float` para garantir compatibilidade com JSON e Chart.js:
- `Decimal` → `float` (valores monetários)
- Listas Python → Arrays JavaScript (via safe filter)
- Strings mantém encoding UTF-8 (nomes de categorias em português)

## Próximos Passos para Frontend Developer

1. Incluir Chart.js CDN no template base ou dashboard
2. Criar elementos `<canvas>` para os gráficos
3. Implementar os scripts usando os dados do context
4. Adicionar responsividade e estilo consistente com o design system
5. Considerar adicionar loading states e mensagens quando não há dados
