# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

# Local imports
from .models import Category
from .forms import CategoryForm


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
        Ordena por tipo de categoria e nome.
        """
        return Category.objects.filter(
            user=self.request.user
        ).order_by('category_type', 'name')

    def get_context_data(self, **kwargs):
        """
        Adiciona categorias separadas por tipo ao contexto.
        """
        context = super().get_context_data(**kwargs)

        # Separa categorias de entrada (receita) e saída (despesa)
        context['income_categories'] = Category.objects.filter(
            user=self.request.user,
            category_type=Category.INCOME
        ).order_by('name')

        context['expense_categories'] = Category.objects.filter(
            user=self.request.user,
            category_type=Category.EXPENSE
        ).order_by('name')

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
            messages.success(self.request, 'Categoria criada com sucesso!')

            return response

        except IntegrityError:
            # Erro de nome duplicado para o mesmo usuário
            form.add_error('name', 'Você já possui uma categoria com este nome.')
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
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Adiciona título da página ao contexto.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoria'
        return context

    def form_valid(self, form):
        """
        Salva a categoria editada e exibe mensagem de sucesso.
        """
        try:
            # Salva a categoria
            response = super().form_valid(form)

            # Mensagem de sucesso
            messages.success(self.request, 'Categoria atualizada com sucesso!')

            return response

        except IntegrityError:
            # Erro de nome duplicado para o mesmo usuário
            form.add_error('name', 'Você já possui uma categoria com este nome.')
            return self.form_invalid(form)
