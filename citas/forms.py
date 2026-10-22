from django import forms

from .models import Cita, Mascota


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ('nombre', 'especie', 'raza', 'nombre_dueno', 'observaciones')
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Luna'}),
            'especie': forms.TextInput(attrs={'placeholder': 'Ej. Perro'}),
            'raza': forms.TextInput(attrs={'placeholder': 'Ej. Mestiza'}),
            'nombre_dueno': forms.TextInput(
                attrs={'placeholder': 'Nombre completo del tutor'}
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Alergias, antecedentes, comportamiento u otra información relevante...',
                }
            ),
        }


class AtencionCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ('sintomas', 'diagnostico')
        widgets = {
            'sintomas': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Describe los síntomas observados o reportados...',
                }
            ),
            'diagnostico': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Escribe el diagnóstico clínico...',
                }
            ),
        }
