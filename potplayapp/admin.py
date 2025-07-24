# potplayapp/admin.py

from django.contrib import admin
from .models import Categoria, Jogo

# Registra o modelo Categoria para que ele apareça no admin
admin.site.register(Categoria)

# Registra o modelo Jogo para que ele apareça no admin
admin.site.register(Jogo)