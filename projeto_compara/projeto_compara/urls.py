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
    path('', lista_produtos, name='lista_produtos'),
    path('cadastrar_produtos/', cadastrar_produtos, name="cadastrar_produtos"),
    path('mercados/', lista_mercados, name='mercados'),
    path('cadastrar_mercados/', cadastrar_mercados, name="cadastrar_mercados"),
    path('tela_precos/<int:id>', tela_precos, name="tela_precos"),
    path('adicionar_precos/<int:id>', adicionar_precos, name="adicionar_precos"),
    path('cadastro/', cadastro, name='cadastro'),
    path('logar', logar, name="logar"),
    path('deslogar', deslogar, name="deslogar"),
    path('mudar_senha', mudar_senha, name='mudar_senha'),
    path('produtos_por_sessao/<int:id_sessao>/', produtos_por_sessao, name='produtos_por_sessao'),
    path('adicionar_categoria/', adicionar_categoria, name="adicionar_categoria"),
    path('excluir_categoria/<int:id_categoria>/', excluir_categoria, name="excluir_categoria"),
    path('cadastro_sessoes/', cadastro_sessoes, name='cadastro_sessoes'),
    path('excluir_sessoes/<int:id_sessoes>', excluir_sessoes, name='excluir_sessoes'),
    path('cadastrar_cidade/', cadastrar_cidade, name="cadastrar_cidade"),
    path('excluir_cidade/<int:id_cidade>', excluir_cidade, name="excluir_cidade"),
    path('editar_cidade/<int:id_cidade>', editar_cidade, name='editar_cidade'),
    path('editar_sessao/<int:id_sessao>', editar_sessao, name='editar_sessao'),
    path('excluir_mercado/<int:id_mercado>', excluir_mercado, name="excluir_mercado"),
    path('editar_mercado/<int:id_mercado>', editar_mercado, name="editar_mercado"),
    path('editar_categoria/<int:id_categoria>', editar_categoria, name="editar_categoria"),
    path('tela_autorizacao/', tela_autorizacao, name='tela_autorizacao'),
    path('autorizar_desautorizar/<int:id_usuario>', autorizar_desautorizar, name='autorizar_desautorizar')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
