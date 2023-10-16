from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category', views.delete_category, name='delete_category'),
    path('update/<int:todo_id>', views.update, name='update'),
    path('delete/<int:todo_id>', views.delete, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('update_settings/', views.update_settings, name='update_settings'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('statistics', views.statistics, name='statistics'),
]