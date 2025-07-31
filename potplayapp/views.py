# potplayapp/views.py
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Jogo, Comentario, Avaliacao, Categoria
from .forms import JogoForm, UserUpdateForm, ComentarioForm, CustomUserCreationForm, AvaliacaoForm

# View para a página inicial (Catálogo de Jogos)
# View para a página inicial (Catálogo de Jogos)
def home_view(request):
    lista_jogos = Jogo.objects.all()
    
    # Verifica se o usuário está logado e se pertence ao grupo 'Avaliadores'
    is_avaliador = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Avaliadores').exists():
            is_avaliador = True
            
    contexto = {
        'jogos': lista_jogos,
        'is_avaliador': is_avaliador  # Passa a informação para o template
    }
    return render(request, 'home.html', contexto)

# View para o cadastro de novos usuários e opção de tipo de perfil
def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Adiciona o usuário ao grupo selecionado
            tipo_perfil = form.cleaned_data.get('tipo_perfil')
            if tipo_perfil == 'desenvolvedor':
                grupo = Group.objects.get(name='Desenvolvedores')
                user.groups.add(grupo)
            elif tipo_perfil == 'avaliador':
                grupo = Group.objects.get(name='Avaliadores')
                user.groups.add(grupo)

            login(request, user)
            return redirect('perfil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

# View para o login de usuários
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('perfil')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# View para o logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View para exibir o perfil do usuário (READ do CRUD de usuário)
@login_required
def perfil_view(request):
    jogos_criados = Jogo.objects.filter(desenvolvedor=request.user)
    return render(request, 'perfil.html', {'jogos_criados': jogos_criados})

# View para alterar o perfil (UPDATE do CRUD de usuário)
@login_required
def alterar_perfil_view(request):
    if request.method == 'POST':
        # Verifica se o formulário de dados do usuário foi enviado
        if 'update_info' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                # (Opcional) Adicionar uma mensagem de sucesso aqui
                return redirect('perfil')
        
        # Verifica se o formulário de alteração de senha foi enviado
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # Mantém o usuário logado após a mudança de senha
                update_session_auth_hash(request, user)
                # (Opcional) Adicionar uma mensagem de sucesso aqui
                return redirect('perfil')

    # Se não for POST, apenas cria os formulários vazios
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    
    contexto = {
        'user_form': user_form,
        'password_form': password_form
    }
    return render(request, 'alterar_perfil.html', contexto)

# View para adicionar um novo jogo (CREATE do CRUD multi-tabelas)
@login_required
def adicionar_jogo_view(request):
    # Verificação de permissão: o usuário pertence ao grupo 'Desenvolvedores'?
    if not request.user.groups.filter(name='Desenvolvedores').exists():
        # Se não pertencer, retorna um erro de acesso negado.
        return HttpResponseForbidden("Você não tem permissão para adicionar jogos.")

    if request.method == 'POST':
        # ... (o resto da sua view continua igual)
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            novo_jogo = form.save(commit=False)
            novo_jogo.desenvolvedor = request.user
            novo_jogo.save()
            return redirect('perfil')
    else:
        form = JogoForm()
    return render(request, 'adicionar_jogo.html', {'form': form})

@login_required
def deletar_jogo_view(request, jogo_id):
    jogo = get_object_or_404(Jogo, pk=jogo_id)

    # --- LÓGICA DE PERMISSÃO ATUALIZADA ---
    # Permite a deleção se o usuário for o dono do jogo OU se pertencer ao grupo 'Avaliadores'.
    
    is_dono = jogo.desenvolvedor == request.user
    is_avaliador = request.user.groups.filter(name='Avaliadores').exists()

    if not (is_dono or is_avaliador):
        # Se não for nem dono, nem avaliador, nega o acesso.
        return HttpResponseForbidden("Você não tem permissão para deletar este jogo.")

    if request.method == 'POST':
        jogo.delete()
        # (Opcional) Adicionar mensagem de sucesso
        # Redireciona para a home, pois um avaliador pode ter vindo de lá.
        return redirect('home') 

    return render(request, 'deletar_jogo_confirmacao.html', {'jogo': jogo})

# View para a página de feed de comentários (Frame 7)
@login_required 
def todos_comentarios_view(request):
    # Busca todos os comentários, ordenando pelos mais recentes
    comentarios = Comentario.objects.all().order_by('-data_criacao')
    return render(request, 'todos_comentarios.html', {'comentarios': comentarios})


# View para adicionar um comentário (Frame 8)
@login_required
def adicionar_comentario_view(request, jogo_id):
    jogo = Jogo.objects.get(pk=jogo_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.jogo = jogo
            novo_comentario.autor = request.user
            novo_comentario.save()
            # Redireciona para o feed geral de comentários após o envio
            return redirect('todos_comentarios')
    else:
        form = ComentarioForm()
        
    return render(request, 'adicionar_comentario.html', {'form': form, 'jogo': jogo})

@login_required
def deletar_comentario_view(request, comentario_id):
    # Busca o comentário específico ou retorna um erro 404
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    # VERIFICAÇÃO DE PERMISSÃO: O usuário logado é o autor do comentário?
    if comentario.autor != request.user:
        return HttpResponseForbidden("Você não tem permissão para deletar este comentário.")

    if request.method == 'POST':
        # Se o formulário de confirmação foi enviado, deleta o comentário
        comentario.delete()
        # Redireciona de volta para a página de onde o usuário provavelmente veio
        return redirect('todos_comentarios')

    # Se o método for GET, mostra a página de confirmação
    return render(request, 'deletar_comentario_confirmacao.html', {'comentario': comentario})

# NOVA VIEW: Página para um avaliador aprovar ou rejeitar um jogo (UPDATE)
@login_required
def avaliar_jogo_view(request, jogo_id):
    # 1. Verifica se o usuário pertence ao grupo 'Avaliadores'
    if not request.user.groups.filter(name='Avaliadores').exists():
        return HttpResponseForbidden("Você não tem permissão para avaliar jogos.")

    jogo = Jogo.objects.get(pk=jogo_id)
    form = AvaliacaoForm()

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)

        # 2. Verifica qual botão foi clicado: 'aprovar' ou 'rejeitar'
        if form.is_valid():
            if 'aprovar' in request.POST:
                jogo.status_avaliacao = 'Aprovado'
            elif 'rejeitar' in request.POST:
                jogo.status_avaliacao = 'Rejeitado'
            
            # 3. Salva o novo status no jogo (AQUI ACONTECE O UPDATE)
            jogo.save()

            # 4. Cria o registro da avaliação
            nova_avaliacao = form.save(commit=False)
            nova_avaliacao.jogo = jogo
            nova_avaliacao.avaliador = request.user
            nova_avaliacao.save()

            # (Opcional) Adicionar mensagem de sucesso
            return redirect('home') # Redireciona para a home após avaliar

    contexto = {
        'jogo': jogo,
        'form': form
    }
    return render(request, 'avaliar_jogo.html', contexto)

@login_required
def editar_jogo_view(request, jogo_id):
    # Busca o jogo a ser editado
    jogo = get_object_or_404(Jogo, pk=jogo_id)

    # VERIFICAÇÃO DE PERMISSÃO: Apenas o desenvolvedor que criou o jogo pode editá-lo.
    if jogo.desenvolvedor != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este jogo.")

    if request.method == 'POST':
        # Passamos 'instance=jogo' para que o formulário saiba que está editando um jogo existente.
        # Também passamos request.FILES para lidar com o upload de um novo arquivo.
        form = JogoForm(request.POST, request.FILES, instance=jogo)
        if form.is_valid():
            form.save()
            # (Opcional) Adicionar mensagem de sucesso
            return redirect('perfil')
    else:
        # Se não for POST, apenas exibe o formulário preenchido com os dados atuais do jogo.
        form = JogoForm(instance=jogo)

    return render(request, 'editar_jogo.html', {'form': form, 'jogo': jogo})