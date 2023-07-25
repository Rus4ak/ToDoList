from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.Register.as_view(), name='signup'),
    path('logout/', views.Logout.as_view(), name='logout')
]
