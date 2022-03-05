from email import message
from tkinter import Menu
from urllib.request import Request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import FormContato

def entrar(request):
    if request.method != 'POST':
        return render(request, 'entrar.html')

    user = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user_valida = auth.authenticate(username=user, password=senha)

    if not user_valida:
        messages.error(request, 'Usuario ou senha invalidos.')
        return render(request, 'entrar.html')

    auth.login(request, user_valida)
    messages.success(request, 'Login feito com sucesso!')
    return redirect('dashboard')


def sair(request):   
    auth.logout(request)

    return redirect('entrar')

def cadastrar(request):
    if request.method != 'POST':
        messages.info(request, 'Preencha os campos.')
        return render(request, 'cadastrar.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuário = request.POST.get('usuario')
    email = request.POST.get('email')
    senha1 = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not usuário or not email or not senha1 or not senha2:
        messages.error(request, 'Todos os campos devem ser preenchidos.')
        return render(request, 'cadastrar.html')

    if len(senha1) < 6:
        messages.error(request, 'Senha deve ter 6 caracteres ou mais.')
        return render(request, 'cadastrar.html')

    if len(usuário) < 6:
        messages.error(request, 'Usuario deve ter 6 caracteres ou mais.')
        return render(request, 'cadastrar.html')

    if senha1 != senha2:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'cadastrar.html')

    if User.objects.filter(username=usuário).exists():
        messages.error(request, 'Usuário já existe!')
        return render(request, 'cadastrar.html')


    user = User.objects.create_user(
        username=usuário,
        email=email,
        password=senha1, 
        first_name=nome,
        last_name=sobrenome
        )

    user.save()
    messages.success(request, 'Cadastro concluído!')
    return redirect('entrar')

@login_required(redirect_field_name='entrar',login_url='entrar')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'dashboard.html', {'dados': form})
    
    form = FormContato(request.POST, request.FILES)
    
    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulario.')
        form = FormContato(request.POST, request.FILES)
        return render(request, 'dashboard.html', {'dados': form})

    email = request.POST.get('email')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe.')
        form = FormContato(request.POST, request.FILES)
        return render(request, 'dashboard.html', {'dados': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} adicionado!')
    return redirect('dashboard')


