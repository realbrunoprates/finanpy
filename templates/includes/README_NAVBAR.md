# Navbar Component - Finanpy

## Localização
`/home/brunoprates/Documentos/Pycodebr/Study/Projetos_estudos/finanpy/templates/includes/navbar.html`

## Como Usar

Para incluir o navbar em qualquer template, adicione a seguinte linha após a tag `<body>` no arquivo `base.html`:

```html
{% include 'includes/navbar.html' %}
```

### Exemplo de Integração no base.html:

```html
<body class='bg-bg-primary min-h-screen'>
    <!-- Include Navbar -->
    {% if user.is_authenticated %}
        {% include 'includes/navbar.html' %}
    {% endif %}

    <!-- Django Messages -->
    {% if messages %}
    ...
    {% endif %}

    <!-- Main Content -->
    <main class='container mx-auto px-4 md:px-6 lg:px-8 py-8'>
        {% block content %}
        {% endblock %}
    </main>
</body>
```

## Recursos Implementados

### 1. Logo/Brand (Esquerda)
- Logo com gradiente roxo (letra "F")
- Nome "Finanpy" com gradiente no texto
- Link para Dashboard
- Efeito hover com shadow

### 2. Links de Navegação (Centro - Desktop)
- **Dashboard** - URL: `dashboard`
- **Contas** - URL: `accounts:list`
- **Categorias** - URL: `categories:category_list`
- **Transações** - URL: `transactions:list`
- Indicador de página ativa com gradiente
- Efeitos hover suaves

### 3. Menu de Usuário (Direita - Desktop)
- Avatar circular com inicial do nome/email
- Nome completo ou email (truncado)
- Dropdown com animação
- **Ver Perfil** (link placeholder `#`)
- **Editar Perfil** (link placeholder `#`)
- **Sair** (botão com form POST para logout)
- Fechamento automático ao clicar fora

### 4. Menu Mobile (Hambúrguer)
- Ícone hambúrguer que alterna para X
- Menu deslizante completo
- Informações do usuário no topo
- Todos os links de navegação com ícones
- Links de perfil
- Botão de logout
- Fechamento automático ao clicar em links

## Indicador de Página Ativa

O navbar usa `request.resolver_match` para detectar a página atual:

- **Dashboard**: `request.resolver_match.url_name == "dashboard"`
- **Contas**: `request.resolver_match.app_name == "accounts"`
- **Categorias**: `request.resolver_match.app_name == "categories"`
- **Transações**: `request.resolver_match.app_name == "transactions"`

Quando ativo, o link recebe o gradiente roxo completo.

## JavaScript Implementado

### Dropdown de Usuário (Desktop)
- Toggle ao clicar no botão
- Rotação da seta (180°)
- Fechamento ao clicar fora
- Atributos ARIA atualizados

### Menu Mobile
- Toggle do menu completo
- Alternância entre ícones (hambúrguer ↔ X)
- Fechamento automático ao clicar em links
- Atributos ARIA para acessibilidade

## Acessibilidade

- **ARIA Labels**: Todos os botões e links têm labels descritivos
- **ARIA Expanded**: Estados de dropdown atualizados
- **Role Attributes**: Menu items com roles apropriados
- **Keyboard Navigation**: Funcional com Tab e Enter
- **Semantic HTML**: Estrutura semântica correta

## Responsividade

### Desktop (md: 768px+)
- Logo à esquerda
- Links centralizados
- Dropdown de usuário à direita
- Menu mobile oculto

### Mobile (< 768px)
- Logo à esquerda
- Botão hambúrguer à direita
- Links de navegação ocultos
- Menu mobile expansível

## Cores e Design System

Todas as cores seguem o design system do Finanpy:

- **Gradiente primário**: `from-primary-500 to-accent-500`
- **Backgrounds**: `bg-bg-secondary`, `bg-bg-tertiary`
- **Texto**: `text-text-primary`, `text-text-secondary`, `text-text-muted`
- **Status**: `text-error` (logout)
- **Bordas**: `border-bg-tertiary`

## Transições e Animações

- **Hover states**: `transition-all duration-200`
- **Dropdown arrow**: `transform rotate(180deg)`
- **Shadows**: `shadow-lg hover:shadow-xl`
- **Colors**: Smooth color transitions
- **Mobile menu**: Slide in/out

## URLs Utilizadas

Certifique-se de que as seguintes URLs estão configuradas:

```python
# core/urls.py
path('dashboard/', DashboardView.as_view(), name='dashboard'),

# users/urls.py (app_name = 'users')
path('logout/', LogoutView.as_view(), name='logout'),

# accounts/urls.py (app_name = 'accounts')
path('', AccountListView.as_view(), name='list'),

# categories/urls.py (app_name = 'categories')
path('', CategoryListView.as_view(), name='category_list'),

# transactions/urls.py (app_name = 'transactions')
path('', TransactionListView.as_view(), name='list'),
```

## Pendências (TODO)

### Links de Perfil

Os links "Ver Perfil" e "Editar Perfil" estão atualmente com `href='#'`.

Quando as views de perfil forem criadas (Tarefas 5.4 e 5.5), atualize para:

```html
<!-- Ver Perfil -->
<a href='{% url "profiles:detail" %}'>Ver Perfil</a>

<!-- Editar Perfil -->
<a href='{% url "profiles:update" %}'>Editar Perfil</a>
```

## Checklist de Qualidade

- [x] Extends/includes funcionais
- [x] Title block definido (N/A - componente)
- [x] Cores exatas do design system
- [x] Texto em português
- [x] Responsividade mobile-first
- [x] Hover e focus states
- [x] Transições suaves (200ms)
- [x] CSRF token no form de logout
- [x] Labels com for/id (N/A - botões)
- [x] Empty states (N/A)
- [x] Mensagens de erro (N/A)
- [x] Acessibilidade básica
- [x] Component library patterns
- [x] File no diretório correto

## Notas Técnicas

1. **Sticky navbar**: Usa `sticky top-0 z-40` para ficar fixo ao rolar
2. **Backdrop blur**: Efeito de blur no fundo (`backdrop-blur-sm`)
3. **Opacity**: Navbar semi-transparente (`bg-bg-secondary/95`)
4. **User object**: Requer `user` no contexto (já disponível com Django auth)
5. **Profile**: Acessa `user.profile.full_name` (relação 1:1 com Profile model)

## Integração Completa

Para ativar o navbar em todo o site, edite `templates/base.html`:

```html
<body class='bg-bg-primary min-h-screen'>
    <!-- Navbar apenas para usuários autenticados -->
    {% if user.is_authenticated %}
        {% include 'includes/navbar.html' %}
    {% endif %}

    <!-- Resto do conteúdo... -->
</body>
```

Isso garante que o navbar só aparece para usuários logados, enquanto páginas públicas (home, login, signup) não mostram a navegação.
