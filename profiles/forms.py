from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Formulário para edição de perfil do usuário.
    """
    class Meta:
        model = Profile
        fields = ['full_name', 'phone']
        labels = {
            'full_name': 'Nome Completo',
            'phone': 'Telefone'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite seu nome completo...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite seu telefone...'
            }),
        }
