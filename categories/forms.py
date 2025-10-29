from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """
    Formulário para criação e edição de categorias.
    """

    class Meta:
        """Define campos, rótulos e widgets do formulário de categorias."""

        model = Category
        fields = ['name', 'category_type', 'color']
        labels = {
            'name': 'Nome',
            'category_type': 'Tipo',
            'color': 'Cor',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: Alimentação'
            }),
            'category_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Selecione o tipo'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-20 h-12 px-1 py-1 bg-bg-secondary border border-bg-tertiary rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traduzir choices para português
        self.fields['category_type'].choices = [
            ('', 'Selecione o tipo'),
            (Category.INCOME, 'Entrada'),
            (Category.EXPENSE, 'Saída'),
        ]

    def clean_name(self):
        """Validação do campo name."""
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return name
