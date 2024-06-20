from django import forms
from .models import Suscripcion

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['correo']
        
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Suscripcion.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Ya esta suscrito.")
        return correo

