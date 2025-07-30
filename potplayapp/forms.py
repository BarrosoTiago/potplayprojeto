# potplayapp/forms.py
# potplayapp/forms.py

from django.contrib.auth.models import User
from .models import Comentario, Avaliacao
from django import forms
from .models import Jogo
# from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        # Inclui todos os campos do model, exceto o 'desenvolvedor'
        # que será adicionado automaticamente na view.
        fields = ['nome', 'descricao', 'categoria', 'arquivo_jogo']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto'] # Apenas o campo de texto será editável pelo usuário

class CustomUserCreationForm(UserCreationForm):
    # Definindo as opções de perfil
    TIPOS_DE_PERFIL = (
        ('desenvolvedor', 'Quero ser um Desenvolvedor'),
        ('avaliador', 'Quero ser um Avaliador'),
    )
    
    # Campo de múltipla escolha para o perfil
    tipo_perfil = forms.ChoiceField(
        choices=TIPOS_DE_PERFIL, 
        required=True,
        label="Tipo de Perfil"
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


# NOVO FORMULÁRIO: Formulário para a avaliação de um jogo
class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['feedback'] # O avaliador só precisa preencher o feedback.
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }
