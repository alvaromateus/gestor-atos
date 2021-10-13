from .models import Ato, SetorOriginario, Assunto, AssuntoSecundario
from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from ato.forms import AtoFieldForm

class AtoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ano', 'data_documento', 'status', 'setor_originario', 'tipo')
    filter_horizontal = ['documento_alterado','documento_revogado','atos_vinculados', 'assuntos', 'assuntos_secundarios']
    search_fields = ('numero','ano','texto', 'data_documento', 'assuntos__nome')
    list_filter = (('data_inicial', DateRangeFilter), ('data_final', DateRangeFilter),
        'status', 'tipo', 'setor_originario__nome','assuntos__nome',
    )
    exclude = ('ano',)    
    form = AtoFieldForm

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
