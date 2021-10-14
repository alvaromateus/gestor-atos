from .models import Ato, SetorOriginario, Assunto, AssuntoSecundario
from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from ato.forms import AtoFieldForm

class AtoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ano', 'data_documento', 'status', 'setor_originario', 'tipo', 'data_suspensao')
    filter_horizontal = ['documentos_alterados','documentos_revogados','atos_vinculados', 'assuntos', 'assuntos_secundarios']
    search_fields = ('numero','ano','texto', 'data_documento', 'assuntos__nome')
    list_filter = (('data_inicial', DateRangeFilter), ('data_final', DateRangeFilter),
        'status', 'tipo', 'setor_originario__nome','assuntos__nome',
    )
    exclude = ('ano',)    
    form = AtoFieldForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.documentos_revogados:
                documentos = obj.documentos_revogados.all()
                for documento in documentos:
                    temp = Ato.objects.get(id=documento.id)
                    if obj.tipo_revogacao == 0: # revogação total ou parcial
                        temp.status = 1
                    else:
                        temp.status = 2
                    temp.save()
            if obj.documentos_alterados:
                documentos = obj.documentos_alterados.all()
                for documento in documentos:
                    temp = Ato.objects.get(id=documento.id)
                    temp.status = 3
                    temp.save()
        except:
            print("Erro de inserção")

        super(AtoAdmin, self).save_model(request, obj, form, change)

class TipoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)

class SetorOriginarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class AssuntoSecundarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    filter_horizontal = ['assuntos',]

admin.site.register(Ato, AtoAdmin)
admin.site.register(SetorOriginario, SetorOriginarioAdmin)
admin.site.register(Assunto, AssuntoAdmin)
admin.site.register(AssuntoSecundario, AssuntoSecundarioAdmin)
admin.site.site_header = 'Gestor de Atos - DPE/PR'
