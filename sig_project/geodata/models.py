from django.db import models
from django.contrib.auth.models import User


class Universidad(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=[('pública', 'Pública'), ('privada', 'Privada')])
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/universidades/', null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Facultad(models.Model):
    nombre_facultad = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/facultades/', null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_facultad} - {self.universidad.nombre}"

class Carrera(models.Model):
    nombre_carrera = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/carreras/', null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    modalidad_inscripcion = models.CharField(max_length=10, choices=[('anual', 'Anual'), ('semestral', 'Semestral')])
    costo_matricula = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField(null=True, blank=True)  # Duración en años
    facultad = models.ForeignKey(Facultad, on_delete=models.SET_NULL, null=True, blank=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre_carrera


class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, null=True, blank=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True, blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True)
    calificacion = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.calificacion} estrellas"
    
class Favorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, null=True, blank=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True, blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True)
    fecha_agregada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'universidad', 'facultad', 'carrera')

    def __str__(self):
        return f"Favorito de {self.usuario} ({self.universidad or self.facultad or self.carrera})"
