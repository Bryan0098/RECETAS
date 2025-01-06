from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Receta(models.Model):
    # Niveles de dificultad posibles para una receta
    DIFICULTAD_OPCIONES = [
        ('F', 'Fácil'),       # Fácil
        ('M', 'Medio'),       # Medio
        ('D', 'Difícil')      # Difícil
    ]
    
    titulo = models.CharField(max_length=255)
    ingredientes = models.TextField()
    descripcion = models.TextField()
    instrucciones = models.TextField()
    imagen = models.ImageField(upload_to='recetas_images/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    dificultad = models.CharField(max_length=1, choices=DIFICULTAD_OPCIONES, default='F')
    tiempo_preparacion = models.DurationField(default=timedelta(minutes=30))

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.receta.titulo}'


class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario.username} ha marcado como favorita la receta {self.receta.titulo}'


# Para futuras implementaciones:

'''
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class RecetaEtiquetas(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    def __str__(self):
        return f'Etiqueta {self.etiqueta.nombre} para {self.receta.titulo}'
'''