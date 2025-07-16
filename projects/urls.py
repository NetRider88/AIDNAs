from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
    path('category/<slug:category_slug>/', views.projects_by_category, name='projects_by_category'),
] 