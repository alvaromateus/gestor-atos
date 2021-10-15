from django import forms
from .models import Ato
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q

class AtoFieldForm(forms.ModelForm):

    class Media:
        js = ('admin/js/ato.js','admin/js/jquery.js',)

    numero = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )

    def __init__(self,*args,**kwargs):
        super (AtoFieldForm,self ).__init__(*args,**kwargs) # Filtro para somente vigentes, parcialmente revogados e alterados, excluindo a si próprio
        if self.instance.pk is not None: # se está no modo de edição
            q = Q(status__in=[0,2,3]) | Q(id__in=self.instance.documentos_revogados.all())
            self.fields['documentos_revogados'].queryset = Ato.objects.filter(q).exclude(id__exact=self.instance.id) 
            self.fields['documentos_alterados'].queryset = Ato.objects.filter(q).exclude(id__exact=self.instance.id) 
        else: # se está no modo de adição
            q = Q(status__in=[0,2,3])
            self.fields['documentos_revogados'].queryset = Ato.objects.filter(q)
            self.fields['documentos_alterados'].queryset = Ato.objects.filter(q)
            
    def clean(self):
        # validação se há seleção dos atributos quando revogado ou alterado é selecionado
        eh_revogador = self.cleaned_data.get('eh_revogador')        
        if eh_revogador:
            documentos_revogados = self.cleaned_data.get('documentos_revogados')
            tipo_revogacao = self.cleaned_data.get('tipo_revogacao')
            if not documentos_revogados:
                raise forms.ValidationError("Necessário informar no mínimo um documento a ser revogado")
            if not tipo_revogacao in [0,1]:
                raise forms.ValidationError("É preciso informar se o documento foi revogado total ou parcialmente")
        eh_alterador = self.cleaned_data.get('eh_alterador')
        if eh_alterador:
            documentos_alterados = self.cleaned_data.get('documentos_alterados')
            if not documentos_alterados:
                raise forms.ValidationError("Necessário informar no mínimo um documento a ser alterado")
        status = self.cleaned_data.get('status')
        if status == 6 and not self.cleaned_data.get('data_suspensao'): # Se o status for alterado para suspensão e não foi informado data
            raise forms.ValidationError("Necessário informar a data de suspensão do ato")            
        
        return self.cleaned_data