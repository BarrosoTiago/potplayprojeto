# potplayapp/models.py

from django.db import models
from django.contrib.auth.models import User

# Tabela 2: Categoria dos Jogos
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Ex: Puzzle, Ação, Estratégia")

    def __str__(self):
        return self.nome

# Tabela 3: Jogo
class Jogo(models.Model):
    # Relacionamento com a tabela User (1-N): um usuário pode ter vários jogos.
    desenvolvedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jogos_criados")
    
    # Relacionamento com a tabela Categoria (1-N): um jogo pertence a uma categoria.
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=False)
    
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    
    # Campo para o upload do arquivo do jogo, conforme RF005
    arquivo_jogo = models.FileField(upload_to='arquivos_jogos/')
    
    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.nome}" por {self.desenvolvedor.username}'
    

class Comentario(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(verbose_name="Seu comentário")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.autor.username} em "{self.jogo.nome}"'