from django import forms
from .models import Suscripcion, Promocion, Detalle, PromocionDetalle
class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['correo']
        
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Suscripcion.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Ya esta suscrito.")
        return correo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

class DetalleForm(forms.ModelForm):
    class Meta:
        model = Detalle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

class PromocionDetalleForm(forms.ModelForm):
    class Meta:
        model = PromocionDetalle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'