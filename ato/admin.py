from .models import Ato, Tipo, SetorOriginario, Assunto
from django.contrib import admin

class AtoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ano', 'status', 'tipo')
    search_fields = ('numero','ano')    
    list_filter = ('status', 'tipo')

class TipoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)

class SetorOriginarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Ato, AtoAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(SetorOriginario, SetorOriginarioAdmin)
admin.site.register(Assunto, AssuntoAdmin)