# Libs
from rest_framework import serializers

# Models
from . import models
from authentication.serializers import UserSerializer


# ===================================================================
#   SERIALIZERS DE PRODUTO
# ===================================================================

class PartesProdutoSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.PartesProduto
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']


class ProdutoSerializer(serializers.ModelSerializer):
  partes_produto = PartesProdutoSerializer(many=True, read_only=True, source='partes')

  class Meta:
    model = models.Produto
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']


class ProdutoReadSerializer(serializers.ModelSerializer):
  partes_produto = PartesProdutoSerializer(
      many=True, read_only=True, source='partes')

  class Meta:
    model = models.Produto
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']


class ProdutoWriteSerializer(serializers.ModelSerializer):
    imagem = serializers.ImageField(required=False, allow_empty_file=True, allow_null=True)

    class Meta:
        model = models.Produto
        fields = ['nome', 'descricao', 'preco', 'imagem', 'partes']


# ===================================================================
#   SERIALIZERS DE PEDIDO
# ===================================================================

class PedidoItemParteResponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='parte_produto.id', read_only=True)
    nome = serializers.CharField(source='parte_produto.nome', read_only=True)
    preco = serializers.DecimalField(source='parte_produto.preco', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = models.PedidoItemParte
        fields = ['id', 'nome', 'preco', 'quantidade']


# item de pedido
class PedidoItemsResponseSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    configuracao_partes = PedidoItemParteResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.PedidoItems
        fields = ['id', 'codigo', 'produto', 'observacao', 'configuracao_partes', 'data_criacao']
        read_only_fields = ['codigo', 'data_criacao']


# pedido completo
class PedidoResponseSerializer(serializers.ModelSerializer):
    items = PedidoItemsResponseSerializer(many=True, read_only=True)
    cliente = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = models.Pedido
        fields = ['id', 'codigo', 'cliente', 'status', 'status_display', 'observacao_geral', 'items', 'data_criacao']
        read_only_fields = ['codigo', 'data_criacao']


class ItemParteDataSerializer(serializers.Serializer):
    parte = serializers.PrimaryKeyRelatedField(queryset=models.PartesProduto.objects.all())
    quantidade = serializers.IntegerField(min_value=1)


# pedido_item no request
class PedidoItemDataSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=models.Produto.objects.all())
    partes_produto = ItemParteDataSerializer(many=True, required=False, default=[])
    observacoes = serializers.CharField(required=False, allow_blank=True, allow_null=True)


# Serializer para o admin ATUALIZAR apenas o status
class PedidoUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pedido
        fields = ['status']
        

# Criar um novo Pedido
class PedidoCreateSerializer(serializers.ModelSerializer):
    
    pedido_items = PedidoItemDataSerializer(many=True, write_only=True)
    observacao_geral = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = models.Pedido
        fields = ['observacao_geral', 'pedido_items']

    def create(self, validated_data):
        itens_data = validated_data.pop('pedido_items', [])
        
        request_user = self.context['request'].user
        if not request_user or not request_user.is_authenticated:
            raise serializers.ValidationError("Cliente não autenticado.")

        pedido_instance = models.Pedido.objects.create(
            cliente=request_user,
            observacao_geral=validated_data.get('observacao_geral')
        )

        lista_pedido_items_criados = []
        for item_data in itens_data:
            produto_obj = item_data['produto']
            observacao_item = item_data.get('observacoes')
            partes_config_data = item_data.get('partes_produto', [])

            pedido_item_obj = models.PedidoItems.objects.create(
                produto=produto_obj,
                observacao=observacao_item
            )
            lista_pedido_items_criados.append(pedido_item_obj)

            for parte_data in partes_config_data:
                models.PedidoItemParte.objects.create(
                    pedido_item=pedido_item_obj,
                    parte_produto=parte_data['parte'],
                    quantidade=parte_data['quantidade']
                )
        
        if lista_pedido_items_criados:
            pedido_instance.items.set(lista_pedido_items_criados)
        
        return pedido_instance

    def to_representation(self, instance):
        return PedidoResponseSerializer(instance, context=self.context).data


# ===================================================================
#   SERIALIZERS DE CHAT
# ===================================================================

# Fluxo Chat
class ChatFluxoOpcaoSerializer(serializers.ModelSerializer):

  fluxo_destino = serializers.CharField(source='fluxo_destino.etapa_fluxo', read_only=True)

  class Meta:
    model = models.ChatFluxoOpcao
    fields = ['id','fluxo_destino','descricao']
    read_only_fields = ['codigo', 'data_criacao']


class ChatFluxoSerializer(serializers.ModelSerializer):
  opcoes = ChatFluxoOpcaoSerializer(many=True, read_only=True,source='fluxo_opcao')
  class Meta:
    model = models.ChatFluxo
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']
    

class ChatMensagemSerializer(serializers.ModelSerializer):
  autor = UserSerializer(read_only=True)
  class Meta:
    model = models.ChatMensagem
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']