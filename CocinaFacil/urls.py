from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from Recetario.views import *
from accounts.views import *


urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('recetas/', recetas_view, name='recetas'),
    path('perfil/', perfil_view, name='perfil'),
    path('recetas/editar/<int:id>/', receta_edit, name='editar-receta'),
    path('recetas/eliminar/<int:id>/', receta_delete, name='eliminar-receta'),
    path('recetas/crear/', receta_create, name='crear-receta'),
    path('recetas/<int:id>/', detalle_receta, name='detalle-receta'),
    path('recetas/comentar/', comentario_create, name='comentar'),
    path('recetas/comentario/eliminar/<int:id>/', comentario_delete, name='eliminar-comentario'),
    path('recetas/buscar/', buscar_receta, name='buscar-receta'),
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Para poder servir archivos estáticos en desarrollo
