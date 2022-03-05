from django.contrib.messages import add_message
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from .models import Contato
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.order_by('id').filter(ocultar=False)
    paginator = Paginator(contatos, 10)

    pagina_num = request.GET.get('pagina')
    contatos = paginator.get_page(pagina_num)
    return render(request, 'index.html', {
        'lista': contatos
    })


def verContato(request, contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if contato.ocultar:
        raise Http404()

    return render(request, 'detalhe_contato.html', {
        'contato': contato
    })

def buscar(request):
    termo = request.GET.get('termo')
    if termo is None or not termo:
        add_message(
            request,
            messages.ERROR,
            'Não foi possível pesquisar com o campo vazio.'
        )

        return redirect('index')

    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
            nome_completo=campos
        ).filter(ocultar=False).filter(
            Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo))

    paginator = Paginator(contatos, 10)
    cont_contatos = 0
    for contato in contatos:
        cont_contatos += 1

    add_message(
        request,
        messages.SUCCESS,
        f'{cont_contatos} Contatos encontrado(s).'
        )
        
    page = request.GET.get('pagina')
    contatos = paginator.get_page(page)
    return render(request, 'busca.html', {
    'lista': contatos
    })