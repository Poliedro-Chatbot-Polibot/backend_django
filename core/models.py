#Django
from django.db import models
#Libs
import shortuuid
from shortuuid.django_fields import ShortUUIDField


def get_path_produto_imagem(instance, filename):
  return f'produtos/{instance.codigo}/{shortuuid.uuid()}.{str(filename).split('.')[len(str(filename).split('.'))-1]}'
def get_path_partes_produto_imagem(instance, filename):
  return f'partes_produto/{instance.codigo}/{shortuuid.uuid()}.{str(filename).split('.')[len(str(filename).split('.'))-1]}'


class Produto(models.Model):
  codigo        = ShortUUIDField(length=7,max_length=9,prefix="pr",alphabet="abcdefg1234",unique=True,editable=False)
  nome          = models.CharField(max_length=100)
  descricao     = models.TextField(blank=True,null=True)
  preco         = models.DecimalField(max_digits=10, decimal_places=2)
  imagem        = models.ImageField(upload_to='get_path_produto_imagem',max_length=400, null=True)
  partes        = models.ManyToManyField('PartesProduto', blank=True, related_name='produtos_associados')
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.nome
  
  class Meta:
    verbose_name = 'Produto'
    verbose_name_plural = 'Produtos'
    ordering = ['-data_criacao']


class PartesProduto(models.Model):
  codigo        = ShortUUIDField(length=7,max_length=9,prefix="pp",alphabet="abcdefg1234",unique=True,editable=False) 
  nome          = models.CharField(max_length=100)
  descricao     = models.TextField(blank=True,null=True)
  imagem        = models.ImageField(upload_to='get_path_partes_produto_imagem',max_length=400,null=True) 
  preco         = models.DecimalField(max_digits=10, decimal_places=2,default=0)
  ativo         = models.BooleanField(default=True)
  obrigatorio   = models.BooleanField(default=False)
  maximo        = models.PositiveIntegerField(default=1)
  minimo        = models.PositiveIntegerField(default=0)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.nome
  
  class Meta:
    verbose_name = 'Parte do Produto'
    verbose_name_plural = 'Partes do Produto'
    ordering = ['-data_criacao']


class Pedido(models.Model):
  PEDIDO_STATUS_CHOICES = (
    ('P', 'Pendente'),
    ('A', 'Produção'),
    ('R', 'Rejeitado'),
    ('C', 'Cancelado'), 
    ('E', 'Enviado'),   
    ('F', 'Finalizado'),
  )

  codigo = ShortUUIDField(length=7,max_length=9,prefix="pe",alphabet="abcdefg1234",unique=True,editable=False)
  status = models.CharField(choices=PEDIDO_STATUS_CHOICES,default='P',max_length=1)
  cliente = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True)
  observacao_geral = models.TextField(blank=True, null=True)
  items = models.ManyToManyField('PedidoItems', blank=True, related_name='pedidos')
  data_criacao = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Pedido {self.codigo} - Cliente: {self.cliente.get_full_name() if self.cliente else "N/A"} - Status: {self.get_status_display()}'
  
  class Meta:
    verbose_name = 'Pedido'
    verbose_name_plural = 'Pedidos'
    ordering = ['-data_criacao']


class PedidoItems(models.Model):
  codigo = ShortUUIDField(length=7,max_length=9,prefix="it",alphabet="abcdefg1234",unique=True,editable=False)
  produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
  observacao = models.TextField(blank=True, null=True)
  data_criacao = models.DateTimeField(auto_now_add=True)

  partes_selecionadas = models.ManyToManyField(
      PartesProduto,
      through='PedidoItemParte',
      through_fields=('pedido_item', 'parte_produto'),
      blank=True
  )

  def __str__(self):
    return f'Item {self.codigo} - Produto: {self.produto.nome}'
  
  class Meta:
    verbose_name = 'Item do Pedido'
    verbose_name_plural = 'Itens do Pedido'
    ordering = ['-data_criacao']


class PedidoItemParte(models.Model):
  pedido_item = models.ForeignKey(PedidoItems, related_name='configuracao_partes', on_delete=models.CASCADE)
  parte_produto = models.ForeignKey(PartesProduto, on_delete=models.CASCADE)
  quantidade = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f'{self.quantidade}x {self.parte_produto.nome} (Item: {self.pedido_item.codigo})'

  class Meta:
    verbose_name = 'Configuração de Parte do Item'
    verbose_name_plural = 'Configurações de Partes dos Itens'
    unique_together = ('pedido_item', 'parte_produto') 


# Fluxo Chat
class Chat(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="ch", alphabet="abcdefg1234", unique=True, editable=False)

  user          = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True)
  etapa_fluxo   = models.ForeignKey('ChatFluxo', on_delete=models.CASCADE, null=True, blank=True, related_name='fluxo')
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Chat {self.codigo} - {self.user}"

  class Meta:
    verbose_name = 'Chat'
    verbose_name_plural = 'Chats'
    ordering = ['-data_criacao']



class ChatMensagem(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="ms", alphabet="abcdefg1234", unique=True, editable=False)

  chat          = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensagens')
  autor         = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True)
  mensagem      = models.TextField(blank=True, null=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.mensagem

  class Meta:
    verbose_name = 'Chat Mensagem'
    verbose_name_plural = 'Chat Mensagens'
    ordering = ['data_criacao']



class ChatFluxo(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="fl", alphabet="abcdefg1234", unique=True, editable=False)

  etapa_fluxo   = models.CharField(max_length=100,default='')
  resposta      = models.TextField(blank=True, null=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.etapa_fluxo
  
  class Meta:
    verbose_name = 'Chat Fluxo'
    verbose_name_plural = 'Chat Fluxos'
    ordering = ['-data_criacao']

class ChatFluxoOpcao(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="fo", alphabet="abcdefg1234", unique=True, editable=False)

  etapa_fluxo   = models.ForeignKey(ChatFluxo, on_delete=models.CASCADE, related_name='fluxo_opcoes')
  fluxo_destino = models.ForeignKey(ChatFluxo, on_delete=models.CASCADE, related_name='fluxo_opcao_destino', null=True, blank=True)
  descricao     = models.TextField(blank=True, null=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.etapa_fluxo} -> {self.fluxo_destino} = {self.descricao}'
    
  class Meta:
    verbose_name = 'Chat Fluxo Opcao'
    verbose_name_plural = 'Chat Fluxo Opcoes'
    ordering = ['-data_criacao']