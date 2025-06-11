from django.contrib import admin


from . import models

# Register your models here.


admin.site.register(models.Produto)
admin.site.register(models.PartesProduto)
admin.site.register(models.Pedido)
admin.site.register(models.PedidoItems)

admin.site.register(models.Chat)
admin.site.register(models.ChatMensagem)
admin.site.register(models.ChatFluxo)
admin.site.register(models.ChatFluxoOpcao)