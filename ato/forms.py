from django import forms
from .models import AssuntoSecundario
from django.contrib.admin.widgets import FilteredSelectMultiple

class AtoFieldForm(forms.ModelForm):

    class Media:
        js = ('admin/js/ato.js','admin/js/jquery.js',)

    numero = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )


    def clean(self):
        # validação se há seleção dos atributos quando revogado ou alterado é selecionado
        eh_revogador = self.cleaned_data.get('eh_revogador')
        eh_alterador = self.cleaned_data.get('eh_alterador')
        if eh_revogador:
            documento_revogado = self.cleaned_data.get('documento_revogado')
            tipo_revogacao = self.cleaned_data.get('tipo_revogacao')
            if not documento_revogado:
                raise forms.ValidationError("Necessário informar um documento a ser revogado")
            if not tipo_revogacao in [0,1]:
                raise forms.ValidationError("É preciso informar se o documento foi revogado total ou parcialmente")
        if eh_alterador:
            documento_alterado = self.cleaned_data.get('documento_alterado')
            if not documento_alterado:
                raise forms.ValidationError("Necessário informar um documento a ser alterado")
        return self.cleaned_data