from django import forms

from .models import Profile

INPUT_STYLE_CLASSES = (
    'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg '
    'text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 '
    'focus:border-transparent transition-all duration-200'
)


class ProfileForm(forms.ModelForm):
    """
    Formulário para edição de perfil do usuário.
    """
    class Meta:
        """Define campos e widgets usados no formulário de perfil."""

        model = Profile
        fields = ['full_name', 'phone']
        labels = {
            'full_name': 'Nome Completo',
            'phone': 'Telefone'
        }
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                    'placeholder': 'Digite seu nome completo...',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                    'placeholder': 'Digite seu telefone...',
                }
            ),
        }
