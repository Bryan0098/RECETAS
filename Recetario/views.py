from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages

from .models import *
# Create your views here.

def welcome_view(request):
    return render(request, 'Recetario/welcome.html')

def recetas_view(request):
    recetas = Receta.objects.order_by('-fecha_creacion')
    return render(request, 'Recetario/recetas.html', {'recetas': recetas})

def perfil_view(request):
    recetas = Receta.objects.filter(autor_id=request.user.id)
    return render(request, 'Recetario/perfil.html', {'recetas': recetas})

def detalle_receta(request, id):
    try:
        receta = Receta.objects.get(id=id)
        comentarios = Comentario.objects.filter(receta_id=id)
        return render(request, 'Recetario/detalle_receta.html', {'receta': receta, 'comentarios': comentarios})
    except Receta.DoesNotExist:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'La receta no existe'})

@login_required(login_url='/accounts/login/')
def receta_create(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        ingredientes = request.POST['ingredientes']
        descripcion = request.POST['descripcion']
        instrucciones = request.POST['instrucciones']
        dificultad = request.POST['dificultad']
        tiempo_preparacion = request.POST['tiempo_preparacion']
        autor_id = request.POST['autor_id']
        imagen = request.FILES.get('imagen')
        receta = Receta(titulo=titulo, ingredientes=ingredientes, descripcion=descripcion, instrucciones=instrucciones,dificultad=dificultad,
            tiempo_preparacion=timedelta(minutes=int(tiempo_preparacion)), autor_id=autor_id, imagen=imagen)
        receta.save()

        return redirect('perfil')
    else:
        return render(request, 'Recetario/crear_receta.html')

@login_required(login_url='/accounts/login/')  
def receta_edit(request, id):
    if request.user.id != Receta.objects.get(id=id).autor_id:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'No puedes editar esta receta'})
    try:
        receta = Receta.objects.get(id=id)
        if request.method == 'POST':
            receta.titulo = request.POST['titulo']
            receta.ingredientes = request.POST['ingredientes']
            receta.descripcion = request.POST['descripcion']
            receta.instrucciones = request.POST['instrucciones']
            receta.dificultad = request.POST['dificultad']
            tiempo_preparacion = request.POST['tiempo_preparacion']
            tiempo_preparacion = int(float(tiempo_preparacion))

            receta.tiempo_preparacion = timedelta(minutes=tiempo_preparacion)

            nueva_imagen = request.FILES.get('imagen')
            if nueva_imagen:
                receta.imagen = nueva_imagen

            receta.save()
            return redirect('detalle-receta', id=id)
        else:
            # Convertir tiempo_preparacion de timedelta a minutos para la edición
            minutos_preparacion = receta.tiempo_preparacion.total_seconds() / 60 if receta.tiempo_preparacion else 0
            context = {
                'receta': receta,
                'minutos_preparacion': int(minutos_preparacion)  # asegura que el valor sea entero
            }
            return render(request, 'Recetario/editar_receta.html', {'receta': receta})
    except Receta.DoesNotExist:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'La receta no existe'})

@login_required(login_url='/accounts/login/')
def receta_delete (request, id):
    if request.user.id != Receta.objects.get(id=id).autor_id:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'No puedes eliminar esta receta'})
    try:
        receta = Receta.objects.get(id=id)
        receta.delete()
        return redirect('perfil')
    except Receta.DoesNotExist:
        return render(request, 'Recetario/recetas.html', {'mensaje': 'La receta no existe'})

@login_required(login_url='/accounts/login/')   
def comentario_create(request):
    if request.method == 'POST':
        autor_id = request.POST['autor_id']
        receta_id = request.POST['receta_id']
        texto = request.POST['texto']
        comentario = Comentario(autor_id=autor_id, receta_id=receta_id, texto=texto)
        comentario.save()
        return redirect('detalle-receta', id=receta_id)
    else:
        return redirect('recetas')
    
@login_required(login_url='/accounts/login/')
def comentario_delete(request, id):
    try:
        comentario = Comentario.objects.get(id=id)
        receta_id = comentario.receta_id

        if request.user.id == comentario.autor_id or request.user.id == Receta.objects.get(id=receta_id).autor_id:
            comentario.delete()
            return redirect('detalle-receta', id=receta_id)
        else:
            return render(request, 'Recetario/recetas.html', {'mensaje': 'No puedes eliminar este comentario'})
    except Comentario.DoesNotExist:
        return redirect('detalle-receta', id=receta_id)
   
""" def buscar_receta(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        nombre = Receta.objects.filter(titulo__contains=titulo)
        ingredientes = Receta.objects.filter(ingredientes__contains=titulo)
        descripcion = Receta.objects.filter(descripcion__contains=titulo)
        recetas = nombre.union(ingredientes, descripcion)

        if recetas.count() == 0:
            return render(request, 'Recetario/recetas.html', {'recetas': recetas, 'mensaje': 'No se encontraron resultados'})
        
        return render(request, 'Recetario/recetas.html', {'recetas': recetas})

    else:
        return redirect('recetas') """


def buscar_receta(request):
    if request.method == 'POST':
        search_value = request.POST.get('search_value', '')
        search_type = request.POST.get('search_type', 'titulo' )

        q_objects = Q()

        if search_type in ['titulo', 'ingredientes', 'descripcion']:
            q_objects &= Q(**{f'{search_type}__icontains': search_value})
        elif search_type in ['F', 'M', 'D']:  # Asume que el formulario envía 'F', 'M', 'D' para dificultades
            q_objects &= Q(dificultad=search_type)
        elif 'tiempo' in search_type:  # Manejo de los tiempos
            if search_type == 'tiempo_0_30':
                q_objects &= Q(tiempo_preparacion__lte=timedelta(minutes=30))
            elif search_type == 'tiempo_30_60':
                q_objects &= Q(tiempo_preparacion__gt=timedelta(minutes=30), tiempo_preparacion__lte=timedelta(minutes=60))
            elif search_type == 'tiempo_60_mas':
                q_objects &= Q(tiempo_preparacion__gt=timedelta(minutes=60))

        recetas = Receta.objects.filter(q_objects)

        if not recetas:
            messages.info(request, 'No se encontraron resultados para tu búsqueda.')

        return render(request, 'Recetario/recetas.html', {'recetas': recetas})

    else:
        return redirect('recetas')
    