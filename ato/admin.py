from .models import Ato, SetorOriginario, Assunto
from django.contrib import admin

class AtoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ano', 'status', 'tipo')
    search_fields = ('numero','ano','texto')
    list_filter = ('status', 'tipo','ano')

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
