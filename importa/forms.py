from django import forms

class ExcelForm(forms.Form):
    archivo_excel = forms.FileField()