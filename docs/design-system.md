# Design System

Guia de estilo visual, paleta de cores e componentes do Finanpy.

## Visão Geral

O Finanpy adota um design moderno em tema escuro com gradientes harmônicos, utilizando TailwindCSS como base. O foco está em criar uma interface limpa, profissional e agradável aos olhos, especialmente para uso prolongado.

## Paleta de Cores

### Cores Primárias

**Gradiente Principal**
```css
/* Gradiente usado em botões principais, headers e elementos de destaque */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Cores Sólidas do Gradiente**
```css
/* Primary - Tom azul/roxo */
primary-500: #667eea
primary-600: #5568d3
primary-700: #4453bd

/* Accent - Tom roxo escuro */
accent-500: #764ba2
accent-600: #63418a
accent-700: #503672
```

### Cores de Fundo (Tema Escuro)

```css
/* Fundo principal da aplicação */
bg-primary: #0f172a      /* slate-900 */

/* Fundo de cards, formulários e elementos */
bg-secondary: #1e293b    /* slate-800 */

/* Fundo de hover e elementos terciários */
bg-tertiary: #334155     /* slate-700 */
```

### Cores de Texto

```css
/* Texto principal - alta legibilidade */
text-primary: #f1f5f9    /* slate-100 */

/* Texto secundário - labels e descrições */
text-secondary: #cbd5e1  /* slate-300 */

/* Texto menos importante - placeholders e hints */
text-muted: #64748b      /* slate-500 */
```

### Cores de Estado

```css
/* Verde - Entradas, sucesso */
success: #10b981         /* emerald-500 */

/* Vermelho - Saídas, erros, exclusões */
error: #ef4444           /* red-500 */

/* Amarelo - Avisos */
warning: #f59e0b         /* amber-500 */

/* Azul - Informações */
info: #3b82f6            /* blue-500 */
```

### Uso das Cores

**Entradas de Dinheiro**: Verde (#10b981)
- Transações de receita
- Indicadores positivos
- Botões de confirmação

**Saídas de Dinheiro**: Vermelho (#ef4444)
- Transações de despesa
- Indicadores negativos
- Botões de exclusão

**Ações Principais**: Gradiente (Primary → Accent)
- Botão de criar/adicionar
- CTAs principais
- Elementos de destaque

**Ações Secundárias**: bg-secondary com borda
- Botões de cancelar
- Ações menos importantes

## Tipografia

### Fonte

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;
```

**Fallback**: Caso Inter não carregue, usa fontes do sistema (system-ui, -apple-system).

### Tamanhos

```css
text-xs: 0.75rem      /* 12px - Muito pequeno, hints */
text-sm: 0.875rem     /* 14px - Textos pequenos, labels */
text-base: 1rem       /* 16px - Texto padrão */
text-lg: 1.125rem     /* 18px - Texto destacado */
text-xl: 1.25rem      /* 20px - Títulos menores */
text-2xl: 1.5rem      /* 24px - Títulos médios */
text-3xl: 1.875rem    /* 30px - Títulos grandes */
text-4xl: 2.25rem     /* 36px - Títulos hero */
```

### Pesos

```css
font-normal: 400      /* Texto normal */
font-medium: 500      /* Texto com destaque leve */
font-semibold: 600    /* Títulos e elementos importantes */
font-bold: 700        /* Grandes destaques */
```

### Hierarquia Tipográfica

```html
<!-- H1 - Títulos de página -->
<h1 class="text-4xl font-bold text-text-primary">Dashboard</h1>

<!-- H2 - Seções -->
<h2 class="text-3xl font-semibold text-text-primary">Transações Recentes</h2>

<!-- H3 - Cards e subseções -->
<h3 class="text-xl font-semibold text-text-primary">Saldo Total</h3>

<!-- Parágrafo padrão -->
<p class="text-base text-text-secondary">Descrição ou conteúdo normal.</p>

<!-- Texto pequeno -->
<span class="text-sm text-text-muted">Informação adicional</span>
```

## Espaçamentos

### Padding e Margin

```css
spacing-1: 0.25rem    /* 4px */
spacing-2: 0.5rem     /* 8px */
spacing-3: 0.75rem    /* 12px */
spacing-4: 1rem       /* 16px */
spacing-6: 1.5rem     /* 24px */
spacing-8: 2rem       /* 32px */
spacing-12: 3rem      /* 48px */
spacing-16: 4rem      /* 64px */
```

### Bordas Arredondadas

```css
rounded-md: 0.375rem    /* 6px - Pequeno */
rounded-lg: 0.5rem      /* 8px - Médio */
rounded-xl: 0.75rem     /* 12px - Grande */
rounded-2xl: 1rem       /* 16px - Extra grande */
```

## Componentes

### Botões

#### Botão Primário

```html
<button class="px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-lg font-medium hover:from-primary-600 hover:to-accent-600 transition-all duration-200 shadow-lg hover:shadow-xl">
    Adicionar Transação
</button>
```

#### Botão Secundário

```html
<button class="px-6 py-3 bg-bg-secondary text-text-primary rounded-lg font-medium hover:bg-bg-tertiary transition-all duration-200 border border-bg-tertiary">
    Cancelar
</button>
```

#### Botão de Sucesso

```html
<button class="px-6 py-3 bg-success text-white rounded-lg font-medium hover:bg-green-600 transition-all duration-200">
    Salvar
</button>
```

#### Botão de Erro/Exclusão

```html
<button class="px-6 py-3 bg-error text-white rounded-lg font-medium hover:bg-red-600 transition-all duration-200">
    Excluir
</button>
```

#### Botão Pequeno

```html
<button class="px-4 py-2 text-sm bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-md font-medium hover:from-primary-600 hover:to-accent-600 transition-all duration-200">
    Editar
</button>
```

### Inputs e Formulários

#### Input Padrão

```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Nome da Conta
    </label>
    <input
        type="text"
        class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
        placeholder="Digite o nome..."
    >
</div>
```

#### Select

```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Tipo de Conta
    </label>
    <select class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200">
        <option>Conta Corrente</option>
        <option>Poupança</option>
        <option>Carteira</option>
    </select>
</div>
```

#### Textarea

```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Descrição
    </label>
    <textarea
        rows="4"
        class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
        placeholder="Digite a descrição..."
    ></textarea>
</div>
```

### Cards

#### Card Padrão

```html
<div class="bg-bg-secondary rounded-xl p-6 shadow-lg border border-bg-tertiary">
    <h3 class="text-xl font-semibold text-text-primary mb-4">Título do Card</h3>
    <p class="text-text-secondary">Conteúdo do card aqui...</p>
</div>
```

#### Card com Gradiente (Destaque)

```html
<div class="bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl p-6 shadow-xl">
    <h3 class="text-xl font-semibold text-white mb-2">Saldo Total</h3>
    <p class="text-3xl font-bold text-white">R$ 10.500,00</p>
</div>
```

#### Card de Estatística

```html
<div class="bg-bg-secondary rounded-xl p-6 shadow-lg border border-bg-tertiary hover:border-primary-500 transition-all duration-200">
    <div class="flex items-center justify-between mb-2">
        <span class="text-text-secondary text-sm font-medium">Entradas do Mês</span>
        <span class="text-success text-sm">↑</span>
    </div>
    <p class="text-2xl font-bold text-text-primary">R$ 5.200,00</p>
    <p class="text-text-muted text-xs mt-1">+12% vs mês anterior</p>
</div>
```

### Tabelas

```html
<div class="bg-bg-secondary rounded-xl shadow-lg border border-bg-tertiary overflow-hidden">
    <table class="w-full">
        <thead>
            <tr class="bg-bg-tertiary">
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Data</th>
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Descrição</th>
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Valor</th>
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Ações</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-t border-bg-tertiary hover:bg-bg-tertiary transition-all duration-150">
                <td class="px-6 py-4 text-text-primary">15/01/2024</td>
                <td class="px-6 py-4 text-text-primary">Salário</td>
                <td class="px-6 py-4 text-success font-semibold">R$ 5.000,00</td>
                <td class="px-6 py-4">
                    <button class="text-primary-500 hover:text-primary-400 text-sm font-medium">Editar</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### Menu de Navegação

#### Navbar Horizontal

```html
<nav class="bg-bg-secondary border-b border-bg-tertiary shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
            <div class="flex items-center">
                <span class="text-2xl font-bold bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
                    Finanpy
                </span>
            </div>
            <div class="flex items-center space-x-4">
                <a href="#" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Dashboard</a>
                <a href="#" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Contas</a>
                <a href="#" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Transações</a>
                <button class="px-4 py-2 bg-error text-white rounded-lg text-sm font-medium hover:bg-red-600 transition-all duration-200">
                    Sair
                </button>
            </div>
        </div>
    </div>
</nav>
```

#### Sidebar Vertical

```html
<aside class="w-64 bg-bg-secondary h-screen fixed left-0 top-0 border-r border-bg-tertiary p-6">
    <div class="mb-8">
        <span class="text-2xl font-bold bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
            Finanpy
        </span>
    </div>
    <nav class="space-y-2">
        <a href="#" class="flex items-center px-4 py-3 text-text-primary bg-bg-tertiary rounded-lg font-medium">
            Dashboard
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all duration-200">
            Contas
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all duration-200">
            Categorias
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all duration-200">
            Transações
        </a>
    </nav>
</aside>
```

### Alertas e Mensagens

#### Sucesso

```html
<div class="bg-success/10 border border-success/20 rounded-lg p-4 mb-4">
    <p class="text-success font-medium">Operação realizada com sucesso!</p>
</div>
```

#### Erro

```html
<div class="bg-error/10 border border-error/20 rounded-lg p-4 mb-4">
    <p class="text-error font-medium">Ocorreu um erro. Tente novamente.</p>
</div>
```

#### Aviso

```html
<div class="bg-warning/10 border border-warning/20 rounded-lg p-4 mb-4">
    <p class="text-warning font-medium">Atenção: verifique os dados informados.</p>
</div>
```

#### Informação

```html
<div class="bg-info/10 border border-info/20 rounded-lg p-4 mb-4">
    <p class="text-info font-medium">Informação importante sobre o sistema.</p>
</div>
```

## Grid e Layout

### Container Principal

```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Conteúdo da página -->
</div>
```

### Grid 2 Colunas

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
</div>
```

### Grid 3 Colunas

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
    <div>Coluna 3</div>
</div>
```

### Grid 4 Colunas

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div>Card 1</div>
    <div>Card 2</div>
    <div>Card 3</div>
    <div>Card 4</div>
</div>
```

## Responsividade

### Breakpoints TailwindCSS

```css
sm: 640px    /* Smartphones landscape */
md: 768px    /* Tablets */
lg: 1024px   /* Desktop pequeno */
xl: 1280px   /* Desktop grande */
2xl: 1536px  /* Desktop extra grande */
```

### Padrões Responsivos

**Mobile First**: Sempre começar pelo mobile e adicionar breakpoints para telas maiores.

```html
<!-- Exemplo: Grid responsivo -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- 1 coluna no mobile, 2 no tablet, 3 no desktop -->
</div>

<!-- Exemplo: Padding responsivo -->
<div class="px-4 md:px-6 lg:px-8">
    <!-- Menos padding no mobile, mais em telas grandes -->
</div>

<!-- Exemplo: Texto responsivo -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">
    <!-- Tamanho aumenta com o tamanho da tela -->
</h1>
```

## Transições e Animações

### Padrão de Transição

```css
transition-all duration-200
```

Usar em:
- Hover de botões
- Mudanças de cor
- Mudanças de tamanho
- Aparecimento de elementos

### Exemplos

```html
<!-- Hover suave em botões -->
<button class="... hover:bg-primary-600 transition-all duration-200">

<!-- Hover em links -->
<a href="#" class="... hover:text-primary-500 transition-colors duration-200">

<!-- Hover em cards -->
<div class="... hover:shadow-xl hover:border-primary-500 transition-all duration-200">
```

## Acessibilidade

### Contraste

Todas as combinações de cores seguem WCAG 2.1 Level AA:
- Texto primário (#f1f5f9) em fundo escuro (#0f172a): Excelente contraste
- Texto secundário (#cbd5e1) em fundo escuro: Bom contraste

### Focus States

Sempre incluir estados de foco visíveis:

```html
<input class="... focus:outline-none focus:ring-2 focus:ring-primary-500">
<button class="... focus:outline-none focus:ring-2 focus:ring-primary-500">
```

### Labels

Sempre incluir labels em formulários:

```html
<label for="account-name" class="...">Nome da Conta</label>
<input id="account-name" type="text" class="...">
```

## Ícones (opcional)

Quando necessário, usar biblioteca leve como:
- **Heroicons**: Ícones SVG minimalistas
- **Feather Icons**: Ícones simples e elegantes
- **Lucide**: Fork mantido do Feather

Evitar bibliotecas pesadas como Font Awesome no MVP.

## Checklist de Design

Ao criar uma nova página ou componente:

- [ ] Usa a paleta de cores definida
- [ ] Segue hierarquia tipográfica
- [ ] Responsivo (mobile, tablet, desktop)
- [ ] Transições suaves em interações
- [ ] Estados de hover/focus/active
- [ ] Contraste adequado para acessibilidade
- [ ] Espaçamentos consistentes
- [ ] Bordas arredondadas (rounded-lg ou rounded-xl)
- [ ] Sombras apropriadas (shadow-lg)

## Configuração TailwindCSS

Para usar as cores customizadas, adicionar em `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'primary': {
          500: '#667eea',
          600: '#5568d3',
          700: '#4453bd',
        },
        'accent': {
          500: '#764ba2',
          600: '#63418a',
          700: '#503672',
        },
        'bg-primary': '#0f172a',
        'bg-secondary': '#1e293b',
        'bg-tertiary': '#334155',
        'text-primary': '#f1f5f9',
        'text-secondary': '#cbd5e1',
        'text-muted': '#64748b',
      },
    },
  },
}
```

## Referências

- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Material Design Color System](https://material.io/design/color)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
