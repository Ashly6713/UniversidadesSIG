from django import forms
from .models import Universidad, Facultad, Carrera, Calificacion

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
        fields = [
            'nombre_carrera', 'descripcion', 'imagen', 
            'modalidad_inscripcion', 'costo_matricula', 
            'facultad', 'universidad', 'duracion'
        ]

    def clean(self):
        cleaned_data = super().clean()
        facultad = cleaned_data.get('facultad')
        universidad = cleaned_data.get('universidad')

        if facultad and facultad.universidad != universidad:
            raise forms.ValidationError(
                "La universidad no corresponde a la facultad seleccionada."
            )

        return cleaned_data


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['calificacion', 'comentario']

    calificacion = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    comentario = forms.CharField(widget=forms.Textarea, required=False)