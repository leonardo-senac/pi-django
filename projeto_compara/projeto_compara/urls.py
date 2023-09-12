"""
URL configuration for projeto_compara project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lista_produtos),
    path('cadastrar_produtos/', cadastrar_produtos, name="cadastrar_produtos"),
    path('mercados/', lista_mercados),
    path('cadastrar_mercados/', cadastrar_mercados, name="cadastrar_mercados"),
    path('tela_precos/<int:id>', tela_precos, name="tela_precos"),
    path('adicionar_precos/<int:id>', adicionar_precos, name="adicionar_precos"),
    path('cadastro/', cadastro, name='cadastro'),
    path('logar/', logar, name="logar"),
    path('deslogar', deslogar, name="deslogar"),
    path('adicionar_produto', adicionar_produto, name="adicionar_produto"),
<<<<<<< Updated upstream
    path('produtos_por_sessao/<int:id_sessao>/', produtos_por_sessao, name='produtos_por_sessao'),
=======
    path('adicionar_categoria/', adicionar_categoria, name="adicionar_categoria"),
    path('excluir_categoria/<int:id_categoria>/', excluir_categoria, name="excluir_categoria")
>>>>>>> Stashed changes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
