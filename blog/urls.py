from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('category/<slug:category_slug>/', views.blog_by_category, name='blog_by_category'),
    path('tag/<str:tag>/', views.blog_by_tag, name='blog_by_tag'),
] 