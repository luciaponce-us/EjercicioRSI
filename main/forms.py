from django import forms
from .models import Anime

class FormatoEmisionForm(forms.Form):
    formatoEmision = forms.ChoiceField(
        label="Formato de emisión",
        widget=forms.Select,
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener dinámicamente los formatos de la BD
        formatos = Anime.objects.values_list('formatoEmision', flat=True).distinct().order_by('formatoEmision')
        self.fields['formatoEmision'].choices = [('', '-- Selecciona un formato --')] + [(f, f) for f in formatos]

class ConfirmarCarga(forms.Form):
    confirmar = forms.BooleanField(label="Confirmar carga de datos en la base de datos", required=True)