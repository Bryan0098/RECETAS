#formulario de registro de usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormCrearUsuario(UserCreationForm):
  #email y contraseña
  email = forms.EmailField(required=True)
  password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    help_texts = {k:"" for k in fields}
    labels = {
      'username': 'Usuario',
      'email': 'Correo electrónico',
    }