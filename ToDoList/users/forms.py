from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm password'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
        return user