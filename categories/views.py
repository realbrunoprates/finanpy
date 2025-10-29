# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CategoryForm
# Local imports
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """
    View para listar categorias do usuário logado.
    Separa categorias de receita e despesa no contexto.
    """
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """
        Retorna apenas as categorias do usuário logado.
        Aplica busca por nome se parâmetro 'search' ou 'q' for fornecido.
        Ordena por tipo de categoria e nome.
        """
        queryset = Category.objects.select_related('user').filter(
            user=self.request.user
        )

        # Busca por nome (aceita 'search' ou 'q' como parâmetro)
        search_query = (
            self.request.GET.get('search')
            or self.request.GET.get('q')
        )
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )

        return queryset.order_by('category_type', 'name')

    def get_context_data(self, **kwargs):
        """
        Adiciona categorias separadas por tipo ao contexto.
        Inclui o termo de busca para manter o valor no template.
        """
        context = super().get_context_data(**kwargs)

        # Captura o termo de busca
        search_query = (
            self.request.GET.get('search')
            or self.request.GET.get('q')
        )

        # Aplica busca nas categorias separadas por tipo
        income_queryset = Category.objects.select_related('user').filter(
            user=self.request.user,
            category_type=Category.INCOME
        )
        expense_queryset = Category.objects.select_related('user').filter(
            user=self.request.user,
            category_type=Category.EXPENSE
        )

        # Se houver busca, aplica o filtro
        if search_query:
            income_queryset = income_queryset.filter(
                Q(name__icontains=search_query)
            )
            expense_queryset = expense_queryset.filter(
                Q(name__icontains=search_query)
            )

        context['income_categories'] = income_queryset.order_by('name')
        context['expense_categories'] = expense_queryset.order_by('name')

        # Adiciona o termo de busca ao contexto para manter o valor no input
        context['search_query'] = search_query or ''

        # Breadcrumbs para navegação
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Categorias', 'url': None},
        ]

        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar uma nova categoria.
    Associa automaticamente a categoria ao usuário logado.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:category_list')

    def get_context_data(self, **kwargs):
        """
        Adiciona título da página ao contexto.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Categoria'
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Categorias', 'url': 'categories:category_list'},
            {'label': 'Nova Categoria', 'url': None},
        ]
        return context

    def form_valid(self, form):
        """
        Associa o usuário logado à categoria antes de salvar.
        Trata erro de nome duplicado (unique_together user+name).
        """
        try:
            # Associa o usuário logado
            form.instance.user = self.request.user

            # Salva a categoria
            response = super().form_valid(form)

            # Mensagem de sucesso
            messages.success(
                self.request,
                'Categoria criada com sucesso!',
            )

            return response

        except IntegrityError:
            # Erro de nome duplicado para o mesmo usuário
            form.add_error(
                'name',
                'Você já possui uma categoria com este nome.',
            )
            return self.form_invalid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para editar uma categoria existente.
    Permite apenas edição de categorias do próprio usuário.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:category_list')

    def get_queryset(self):
        """
        Retorna apenas as categorias do usuário logado.
        Garante que o usuário só possa editar suas próprias categorias.
        """
        return Category.objects.select_related('user').filter(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        """
        Adiciona título da página ao contexto.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoria'
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Categorias', 'url': 'categories:category_list'},
            {'label': 'Editar Categoria', 'url': None},
        ]
        return context

    def form_valid(self, form):
        """
        Salva a categoria editada e exibe mensagem de sucesso.
        """
        try:
            # Salva a categoria
            response = super().form_valid(form)

            # Mensagem de sucesso
            messages.success(
                self.request,
                'Categoria atualizada com sucesso!',
            )

            return response

        except IntegrityError:
            # Erro de nome duplicado para o mesmo usuário
            form.add_error(
                'name',
                'Você já possui uma categoria com este nome.',
            )
            return self.form_invalid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir uma categoria existente.
    Permite apenas exclusão de categorias do próprio usuário.
    Previne exclusão de categorias com transações associadas.
    """
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:category_list')

    def get_queryset(self):
        """
        Retorna apenas as categorias do usuário logado.
        Garante que o usuário só possa excluir suas próprias categorias.
        """
        return Category.objects.select_related('user').prefetch_related(
            'transactions'
        ).filter(
            user=self.request.user
        )

    def form_valid(self, form):
        """
        Valida se a categoria pode ser excluída antes de removê-la.
        """
        category = self.object

        if category.transactions.exists():
            messages.error(
                self.request,
                (
                    'Não é possível excluir esta categoria pois ela possui '
                    'transações associadas.'
                ),
            )
            return redirect('categories:category_list')

        messages.success(
            self.request,
            'Categoria excluída com sucesso!',
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adiciona breadcrumbs ao contexto para navegação consistente.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Categorias', 'url': 'categories:category_list'},
            {'label': 'Excluir Categoria', 'url': None},
        ]
        return context
