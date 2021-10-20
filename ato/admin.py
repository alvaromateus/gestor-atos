from .models import Ato, SetorOriginario, Assunto, AssuntoSecundario
from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from ato.forms import AtoFieldForm

class AtoAdmin(admin.ModelAdmin):

    list_display = ('tipo', 'numero', 'ano', 'setor_originario', 'status', 'data_documento', 'data_final', 'data_suspensao')
    filter_horizontal = ['documentos_alterados','documentos_revogados','atos_vinculados', 'assuntos', 'assuntos_secundarios']
    search_fields = ('numero','ano','texto', 'tipo', 'data_documento', 'assuntos__nome', 'setor_originario__nome', 'setor_originario__sigla')
    list_filter = (('data_inicial', DateRangeFilter), ('data_final', DateRangeFilter),
        'status', 'tipo', 'setor_originario__nome','assuntos__nome',
    )
    readonly_fields = ['atos_revogantes', 'atos_alterantes']
    exclude = ('ano',)
    form = AtoFieldForm

    def save_model(self, request, obj, form, change):            
        super(AtoAdmin, self).save_model(request, obj, form, change)
        revogados = Ato.objects.filter(id__in=request.POST.getlist('documentos_revogados'))        
        if revogados:
            for revogado in revogados:
                obj.documentos_revogados.add(revogado)

            documentos = obj.documentos_revogados.all()
            for documento in documentos:
                temp = Ato.objects.get(id=documento.id)
                if obj.tipo_revogacao == 0: # revogação total 
                    temp.status = 1
                else: # revogação parcial
                    temp.status = 2
                temp.save()
        
        alterados = Ato.objects.filter(id__in=request.POST.getlist('documentos_alterados'))
        if alterados:
            for alterado in alterados:
                obj.documentos_alterados.add(alterado)

            documentos = obj.documentos_alterados.all()
            for documento in documentos:
                temp = Ato.objects.get(id=documento.id)
                temp.status = 3
                temp.save()
        

class TipoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)

class SetorOriginarioAdmin(admin.ModelAdmin):
    list_display = ('nome','sigla')

class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    filter_horizontal = ['assuntos_secundarios',]

class AssuntoSecundarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Ato, AtoAdmin)
admin.site.register(SetorOriginario, SetorOriginarioAdmin)
admin.site.register(Assunto, AssuntoAdmin)
admin.site.register(AssuntoSecundario, AssuntoSecundarioAdmin)
admin.site.site_header = 'Gestor de Atos - DPE/PR'
