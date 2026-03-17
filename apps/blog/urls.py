from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.post_create, name='post_create'),
    path('', views.blog_list, name='blog_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug:slug>/editar/', views.post_update, name='post_update'),
    path('<slug:slug>/borrar/', views.post_delete, name='post_delete'),
    
]
