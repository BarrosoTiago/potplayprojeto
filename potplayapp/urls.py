# potplayapp/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import comentarios_json_view

urlpatterns = [
    path('', views.home_view, name='home'),
    # URLs de Autenticação e Usuário
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/alterar/', views.alterar_perfil_view, name='alterar_perfil'),
    
    # URL do CRUD de Jogo (Create)
    path('adicionar_jogo/', views.adicionar_jogo_view, name='adicionar_jogo'),
    
    # mostra comentarios na home
    path('comentarios-json/', comentarios_json_view, name='comentarios_json'),


    # URL para a página GERAL de comentários
    path('comentarios/', views.todos_comentarios_view, name='todos_comentarios'),

    # URL para ADICIONAR um comentário a um JOGO ESPECÍFICO
    path('jogo/<int:jogo_id>/adicionar_comentario/', views.adicionar_comentario_view, name='adicionar_comentario'),

    path('jogo/<int:jogo_id>/favoritar/', views.favoritar_jogo_view, name='favoritar_jogo'),


    # NOVA URL: Rota para a página de avaliação de um jogo específico
    path('jogo/<int:jogo_id>/avaliar/', views.avaliar_jogo_view, name='avaliar_jogo'),

    path('jogo/<int:jogo_id>/deletar/', views.deletar_jogo_view, name='deletar_jogo'),

    # NOVA URL: Rota para a página de confirmação de deleção de um comentário
    path('comentario/<int:comentario_id>/deletar/', views.deletar_comentario_view, name='deletar_comentario'),

    # NOVA URL: Rota para a página de edição de um jogo
    path('jogo/<int:jogo_id>/editar/', views.editar_jogo_view, name='editar_jogo'),
]