from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from accounts.forms import FormCrearUsuario
from .models import *

# Create your views here.

def login_view(request):
  if request.method == 'POST':
    usuario = request.POST['usuario']
    clave = request.POST['clave']
    user = authenticate(request, username=usuario, password=clave)
    if user is not None:
      login(request, user)
      return redirect('welcome')
    else:
      return render(request, 'accounts/login.html', {'mensaje': 'Usuario o clave incorrectos'})
  else:
    if request.user.is_authenticated:
      return redirect('welcome')
    else:
      return render(request, 'accounts/login.html')
    
def register_view(request):
  #usando UserCreationForm
  if request.method == 'POST':
    form = FormCrearUsuario(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
    else:
      return render(request, 'accounts/register.html', {'form': form})
  else:
    form = FormCrearUsuario()
    return render(request, 'accounts/register.html', {'form': form})