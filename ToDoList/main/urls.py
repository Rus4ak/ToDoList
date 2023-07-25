from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-task/', views.create_task, name='create-task'),
    path('mark-done/<int:task_id>/', views.mark_done, name='mark-done'),
    path('view-task/<int:task_id>/', views.view_task, name='view-task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete-task')
]
