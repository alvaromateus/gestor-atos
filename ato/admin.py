from .models import Ato, SetorOriginario, Assunto
from django.contrib import admin
from rangefilter.filters import DateRangeFilter

class AtoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ano', 'status', 'tipo')
    filter_horizontal = ['atos_vinculados', 'assuntos']
    search_fields = ('numero','ano','texto')
    list_filter = (('data_inicial', DateRangeFilter), ('data_final', DateRangeFilter),
        'status', 'tipo', 'setor_originario__nome',
    )

class TipoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)

class SetorOriginarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Ato, AtoAdmin)
admin.site.register(SetorOriginario, SetorOriginarioAdmin)
admin.site.register(Assunto, AssuntoAdmin)
admin.site.site_header = 'Gestor de Atos - DPE/PR'
