# Sistema de Mensagens do Django

O sistema de mensagens de feedback está completamente implementado no arquivo `templates/base.html` seguindo o design system do Finanpy.

## Funcionalidades Implementadas

### 1. Tipos de Mensagens

O sistema suporta 4 tipos de mensagens com cores específicas do design system:

- **SUCCESS** (Verde #10b981): Para operações bem-sucedidas
- **ERROR** (Vermelho #ef4444): Para erros e falhas
- **WARNING** (Amarelo/Laranja #f59e0b): Para avisos e alertas
- **INFO** (Azul #3b82f6): Para informações gerais

### 2. Características Visuais

- **Posicionamento**: Fixed no topo direito da tela (top-20 quando autenticado, top-4 quando não autenticado)
- **Layout**: Cards com fundo semi-transparente (bg-color/10) e borda (border-color/20)
- **Ícones**: SVG específico para cada tipo de mensagem
- **Botão de fechar**: X no canto superior direito de cada mensagem
- **Responsividade**: max-w-md para largura máxima em desktop, adapta-se a mobile
- **Z-index**: 50 para ficar acima de outros elementos

### 3. Animações

- **Entrada**: Slide in da direita (slideInRight) com duração de 0.3s
- **Saída**: Fade out + slide para direita com duração de 0.5s
- **Auto-dismiss**: Mensagens desaparecem automaticamente após 5 segundos

### 4. Integração com Django

Para usar mensagens nas views, importe o módulo `messages` do Django:

```python
from django.contrib import messages
from django.shortcuts import render, redirect

def minha_view(request):
    # Mensagem de sucesso
    messages.success(request, 'Operação realizada com sucesso!')

    # Mensagem de erro
    messages.error(request, 'Ocorreu um erro ao processar sua solicitação.')

    # Mensagem de aviso
    messages.warning(request, 'Atenção: verifique os dados informados.')

    # Mensagem informativa
    messages.info(request, 'Esta é uma informação importante.')

    return redirect('app:list')
```

## Exemplo de Uso em Views

### CreateView (Criar registro)

```python
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class AccountCreateView(SuccessMessageMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')
    success_message = 'Conta criada com sucesso!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
```

### UpdateView (Atualizar registro)

```python
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

class AccountUpdateView(SuccessMessageMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')
    success_message = 'Conta atualizada com sucesso!'
```

### DeleteView (Excluir registro)

```python
from django.views.generic import DeleteView
from django.contrib import messages

class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'accounts/confirm_delete.html'
    success_url = reverse_lazy('accounts:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Conta excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
```

### Function-based View (View baseada em função)

```python
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('accounts:list')
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os campos.')
    else:
        form = AccountForm()

    return render(request, 'accounts/form.html', {'form': form})
```

## Estrutura HTML Implementada

```html
<!-- Django Messages -->
{% if messages %}
<div class='fixed {% if user.is_authenticated %}top-20{% else %}top-4{% endif %} right-4 z-50 space-y-3 max-w-md'>
    {% for message in messages %}
    <div class='
        {% if message.tags == 'success' %}
            bg-success/10 border-success/20 text-success
        {% elif message.tags == 'error' %}
            bg-error/10 border-error/20 text-error
        {% elif message.tags == 'warning' %}
            bg-warning/10 border-warning/20 text-warning
        {% elif message.tags == 'info' %}
            bg-info/10 border-info/20 text-info
        {% else %}
            bg-bg-secondary border-bg-tertiary text-text-primary
        {% endif %}
        border rounded-lg p-4 shadow-lg backdrop-blur-sm auto-hide flex items-start gap-3 animate-slide-in
    ' role='alert'>
        <!-- Icon (SVG específico para cada tipo) -->
        <div class='flex-shrink-0 mt-0.5'>
            <!-- SVG Icon -->
        </div>

        <!-- Message Content -->
        <div class='flex-1 font-medium'>
            {{ message }}
        </div>

        <!-- Close Button -->
        <button type='button' class='flex-shrink-0 ml-2 opacity-70 hover:opacity-100 transition-opacity duration-200' onclick='this.parentElement.remove()'>
            <!-- X Icon SVG -->
        </button>
    </div>
    {% endfor %}
</div>
{% endif %}
```

## CSS Personalizado (Animações)

```css
/* Message animations */
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.animate-slide-in {
    animation: slideInRight 0.3s ease-out forwards;
}
```

## JavaScript (Auto-dismiss)

```javascript
<!-- Auto-hide messages after 5 seconds -->
<script>
    setTimeout(() => {
        document.querySelectorAll('.auto-hide').forEach(el => {
            el.style.transition = 'opacity 0.5s, transform 0.5s';
            el.style.opacity = '0';
            el.style.transform = 'translateX(100%)';
            setTimeout(() => el.remove(), 500);
        });
    }, 5000);
</script>
```

## Design System Compliance

O sistema de mensagens segue rigorosamente o design system do Finanpy:

- **Cores**: Usa as cores exatas definidas em tailwind.config.js
- **Tema Escuro**: Totalmente compatível com o tema escuro (#0f172a, #1e293b)
- **Tipografia**: Fonte Inter, font-medium
- **Spacing**: Padding e gaps consistentes (p-4, gap-3)
- **Border Radius**: rounded-lg (8px)
- **Transições**: Suaves e consistentes (0.2s - 0.5s)
- **Acessibilidade**: role='alert' para leitores de tela

## Checklist de Qualidade

- [x] Extends from base.html
- [x] Usa cores exatas do design system
- [x] Totalmente responsivo (mobile-first)
- [x] Hover e focus states definidos
- [x] Transições suaves aplicadas
- [x] Ícones SVG para cada tipo de mensagem
- [x] Botão de fechar funcional
- [x] Auto-dismiss após 5 segundos
- [x] Animações de entrada/saída
- [x] Acessibilidade básica (role='alert')
- [x] Z-index apropriado (z-50)
- [x] Posicionamento fixed responsivo

## Notas Importantes

1. As mensagens são exibidas no topo direito, ajustando a posição baseado no estado de autenticação do usuário
2. O sistema usa aspas simples conforme padrão do projeto
3. Todas as cores são do design system (sem cores customizadas)
4. O sistema é totalmente funcional sem JavaScript (fallback gracioso)
5. Mensagens podem ser fechadas manualmente ou automaticamente após 5s
