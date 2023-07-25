from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View

from .forms import RegisterForm

# Create your views here.

class Register(FormView):
    form_class = RegisterForm
    success_url = '/profile/login'
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)
    
    def form_invalid(self, form):
        return super(Register, self).form_invalid(form)
    

class Login(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'users/login.html'

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(Login, self).form_valid(form)
    

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('main:index')
    