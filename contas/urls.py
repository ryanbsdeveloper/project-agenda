from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrar, name='entrar'),
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
