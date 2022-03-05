from re import search
from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone',
                    'email', 'data_criacao', 'categoria', 'ocultar')
    list_display_links = ('nome','id')
    list_per_page = 10
    search_fields = ('nome', 'telefone', 'sobrenome')
    list_editable = ['ocultar']


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
