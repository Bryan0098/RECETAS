from django.contrib import admin

# Register your models here.

# Todos lo usuarion podrán en sus propias recetas editar, eliminar y crear recetas.

from .models import Receta, Comentario, Favorito

admin.site.register(Receta)
admin.site.register(Comentario)
admin.site.register(Favorito)