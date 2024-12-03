from django.urls import path
from . import views

urlpatterns = [
    path('cotacao/', views.cotacao, name='cotacao'),
    path('cotacao/<str:code_codein>/', views.cotacao_detalhe, name='cotacao_detalhe'),
]
