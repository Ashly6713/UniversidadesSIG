from django import forms
from .models import Point, Universidad, Facultad, Carrera, Calificacion

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['name', 'description', 'image']
        

class UniversidadForm(forms.ModelForm):
    class Meta:
        model = Universidad
        fields = ['nombre', 'tipo', 'descripcion', 'imagen']


class FacultadForm(forms.ModelForm):
    class Meta:
        model = Facultad
        fields = ['nombre_facultad', 'descripcion', 'imagen', 'universidad']


class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre_carrera', 'descripcion', 'imagen', 'modalidad_inscripcion', 'costo_matricula', 'facultad', 'universidad', 'duracion']


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['calificacion', 'comentario']

    calificacion = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    comentario = forms.CharField(widget=forms.Textarea, required=False)