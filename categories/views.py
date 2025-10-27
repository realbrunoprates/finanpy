# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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
