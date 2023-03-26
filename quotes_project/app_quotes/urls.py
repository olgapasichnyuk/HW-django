from django.urls import path
from . import views

app_name = 'app_quotes'

urlpatterns = [
    path('', views.main, name='main'),

    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.add_quote, name='quote'),
    path('author/<int:pk>', views.author_detail, name='author_detail'),
]
