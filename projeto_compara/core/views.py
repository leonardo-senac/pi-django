from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import *

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

@login_required(login_url="/logar")
def cadastro_sessoes(request):
    sessoes = Sessão.objects.all()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Sessão.objects.create(nome=nome)
    return render(request, 'cadastro_sessoes.html', {'sessoes': sessoes, 'usuario': request.user})

@login_required(login_url="/logar")
def cadastrar_produtos(request):
    sessoes = Sessão.objects.all()
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nome_produto = request.POST.get('nome')
        produto_descricao = request.POST.get('descricao')
        id_categoria = request.POST.get('categoria')

        produto_categoria = Categoria.objects.get(id=id_categoria)

        Produto.objects.create(nome= nome_produto, descricao=produto_descricao, categoria=produto_categoria)
    return render(request, 'cadastro_produto.html', {'sessoes': sessoes, 'categorias': categorias, 'usuario': request.user})

@login_required(login_url="/logar")
def lista_mercados(request):
    usuario = request.user
    mercados = Mercado.objects.all()
    cidades = Cidade.objects.all()
    sessoes = Sessão.objects.all()
    # rua = Mercado.object.all()
    # cidade = Mercado.objects.all()
    return render(request, 'mercados.html', {'mercados': mercados, 'cidades': cidades, 'sessoes': sessoes, 'usuario': usuario})


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
    return render(request, 'produtos.html', {'produtos': produtos, 'categorias':categorias, 'precos': precos, 'usuario': usuario, 'sessoes': sessoes, 'usuario': request.user})

@login_required(login_url="/logar")
def cadastrar_mercados(request):
    nome_mercado = request.POST.get('nome')
    rua_mercado = request.POST.get('rua')
    bairro_mercado = request.POST.get('bairro')
    numero_mercado = request.POST.get('numero')

    id_cidade = request.POST.get('cidade')

    cidade_mercado = Cidade.objects.get(id=id_cidade)
     
    Mercado.objects.create(nome=nome_mercado, rua=rua_mercado, cidade=cidade_mercado, bairro=bairro_mercado,numero=numero_mercado)
    return redirect(lista_mercados)

@login_required(login_url="/logar")
def editar_mercado(request, id_mercado):
    mercado = Mercado.objects.get(id=id_mercado)

    mercado.nome = request.POST.get('nome')
    mercado.rua = request.POST.get('rua')
    mercado.bairro = request.POST.get('bairro')
    mercado.numero = request.POST.get('numero')
    mercado.cidade = Cidade.objects.get(id=request.POST.get('cidade'))

    mercado.save()

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

@login_required(login_url="/logar")
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

@login_required(login_url="/logar")
def adicionar_categoria(request):
    categorias = Categoria.objects.all()
    sessoes = Sessão.objects.all()
    if request.method == 'POST':
        nome = request.POST['nome']
        sessao = Sessão.objects.get(id=request.POST['sessao'])
        Categoria.objects.create(nome=nome, sessao=sessao)
    return render(request, 'categoria.html', {"categorias": categorias, 'sessoes': sessoes, 'usuario': request.user})    

@login_required(login_url="/logar")
def excluir_categoria(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    categoria.delete()
    return redirect(adicionar_categoria)

@login_required(login_url="/logar")
def excluir_mercado(request, id_mercado):
    mercado = Mercado.objects.get(id=id_mercado)
    mercado.delete()
    return redirect(lista_mercados)

@login_required(login_url="/logar")
def excluir_sessoes(request, id_sessoes):
    sessoes =  Sessão.objects.get(id=id_sessoes)

    sessoes.delete()

    return redirect(cadastro_sessoes)

@login_required(login_url="/logar")
def cadastrar_cidade(request):
    cidades = Cidade.objects.all()
    if request.method == 'POST':
        nome = request.POST['nome']
        Cidade.objects.create(nome=nome)
    return render(request, 'cidades.html', {"cidades": cidades, 'usuario': request.user, 'sessoes': Sessão.objects.all()})

@login_required(login_url="/logar")
def excluir_cidade(request, id_cidade):
    cidades =  Cidade.objects.get(id=id_cidade)

    cidades.delete()
    return redirect(cadastrar_cidade)

@login_required(login_url="/logar")
def editar_cidade(request,id_cidade):
    cidade=Cidade.objects.get(id=id_cidade)
    cidade.nome = request.POST['nome']

    cidade.save()

    return redirect(cadastrar_cidade)


@login_required(login_url="/logar")
def editar_sessao(request,id_sessao):
    sessao=Sessão.objects.get(id=id_sessao)
    sessao.nome = request.POST['nome']

    sessao.save()

    return redirect(cadastro_sessoes)

def mudar_senha(request):
    usuario = User.objects.get(id=request.user.id)
    if usuario.check_password(request.POST['senha_antiga']):
        usuario.password = make_password(request.POST['nova_senha'])
        usuario.save()
        alert = 'Senha alterada com sucesso!'
    else:
        alert = 'Erro na senha atual!'
    return redirect(lista_produtos)