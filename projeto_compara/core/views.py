from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def lista_produtos(request):
    produtos = Produto.objects.all().order_by('nome')
    categorias = Categoria.objects.all()
    sessoes = Sessão.objects.all()
    precos = []
    for produto in produtos:
        preco_produto = produtos_mercados.objects.filter(produto=produto).order_by('preco')
        precos.append(preco_produto)
    usuario = request.user
    return render(request, 'produtos.html', {'produtos': produtos, 'categorias':categorias, 'precos': precos, 'usuario': usuario, 'sessoes': sessoes})

def cadastrar_produtos(request):
    nome_produto = request.POST.get('nome')
    produto_descricao = request.POST.get('descricao')
    id_categoria = request.POST.get('categoria')

    produto_categoria = Categoria.objects.get(id=id_categoria)

    Produto.objects.create(nome= nome_produto, descricao=produto_descricao, categoria=produto_categoria)
    return redirect(lista_produtos)

def lista_mercados(request):
    mercados = Mercado.objects.all()
    cidades = Cidade.objects.all()
    sessoes = Sessão.objects.all()
    # rua = Mercado.object.all()
    # cidade = Mercado.objects.all()
    return render(request, 'mercados.html', {'mercados': mercados, 'cidades': cidades, 'sessoes': sessoes})


def produtos_por_sessao(request, id_sessao):
    sessao = Sessão.objects.get(id=id_sessao)
    produtos = Produto.objects.filter(categoria__sessao=sessao).order_by('nome')
    categorias = Categoria.objects.all()
    sessoes = Sessão.objects.all()
    precos = []
    for produto in produtos:
        preco_produto = produtos_mercados.objects.filter(produto=produto).order_by('preco')
        precos.append(preco_produto)
    usuario = request.user
    return render(request, 'produtos.html', {'produtos': produtos, 'categorias':categorias, 'precos': precos, 'usuario': usuario, 'sessoes': sessoes})


def cadastrar_mercados(request):
    nome_mercado = request.POST.get('nome')
    rua_mercado = request.POST.get('rua')
    bairro_mercado = request.POST.get('bairro')
    numero_mercado = request.POST.get('numero')

    id_cidade = request.POST.get('cidade')

    cidade_mercado = Cidade.objects.get(id=id_cidade)
     
    Mercado.objects.create(nome=nome_mercado, rua=rua_mercado, cidade=cidade_mercado, bairro=bairro_mercado,numero=numero_mercado)
    return redirect(lista_mercados)

def tela_precos(request, id):
    produto = Produto.objects.get(id=id)
    mercados = Mercado.objects.all()
    mercados_produtos = produtos_mercados.objects.filter(produto = produto)
    sessoes = Sessão.objects.all()
    usuario = request.user
    precificados = []
    for linha in mercados_produtos:
        precificados.append(linha.mercado)
        linha.preco = float(linha.preco)

    return render(request, 'precos.html', {'produto': produto, 'mercados': mercados, 'mercados_produtos': mercados_produtos, 'precificados': precificados, 'sessoes': sessoes, 'usuario': usuario})

def adicionar_precos(request, id):
    mercados = Mercado.objects.all()
    produto = Produto.objects.get(id=id)
    for mercado in mercados:
        preco_mercado = request.POST.get(f'{mercado.id}')
        try:
            existencia = produtos_mercados.objects.get(mercado=mercado, produto=produto)
            existencia.preco = preco_mercado
            existencia.save()
        except:
            if float(preco_mercado) > 0:
                produtos_mercados.objects.create(mercado=mercado, produto=produto, preco=preco_mercado)
    return redirect(lista_produtos)

def cadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('cadastro')
    return render(request, 'cadastro.html')

def logar(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect(lista_produtos)
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})

def deslogar(request):
    logout(request)
    return redirect(lista_produtos)

def adicionar_produto(request):
    return redirect(lista_produtos)

def lista_sessoes(request):
    # Recupere todas as sessões do banco de dados
    sessoes = Sessão.objects.all()
    return render(request, 'lista_sessoes.html', {'sessoes': sessoes})

