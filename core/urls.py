# core/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r'produto', views.ProdutoViewSet, basename='produto')
router.register(r'partes-produto', views.PartesProdutoViewSet, basename='parteproduto')
router.register(r'pedido', views.PedidoViewSet, basename='pedido') # <- O erro estava aqui
router.register(r'pedido-items', views.PedidoItemsViewSet, basename='pedidoitem')

urlpatterns = [
  path('', include(router.urls)),
  path('chat', views.ChatApiView.as_view(), name='chat_api'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)