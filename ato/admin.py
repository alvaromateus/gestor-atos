from .models import *
from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from ato.forms import AtoFieldForm
from reportlab.pdfgen import canvas

class AtoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'numero', 'ano', 'setor_originario', 'status', 'data_documento','publicacao')
    filter_horizontal = ['documentos_alterados','documentos_revogados','atos_vinculados', 'assuntos', 'assuntos_secundarios']
    search_fields = ('numero','ano','texto', 'tipo', 'data_documento', 'assuntos__nome', 'setor_originario__nome', 'setor_originario__sigla')
    list_filter = (('data_inicial', DateRangeFilter), ('data_final', DateRangeFilter),
        'status', 'tipo', 'setor_originario__nome','assuntos__nome', 'publicacao',
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

class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'data')
    change_form_template = 'change_form.html'

    def response_change(self, request, obj):
        id = obj.id
        atos = Ato.objects.filter(publicacao=obj)
        if "gerar_pdf_publicacao" in request.POST:
            nome_pdf = 'publicacao_'+str(obj.numero)
            pdf = canvas.Canvas('media/publicacoes/{}.pdf'.format(nome_pdf))
            pdf.drawString(20,750, str(obj)) # título da Publicação
            x = 720
            for ato in atos:
                x -= 40
                pdf.drawString(20,x, '{}'.format(ato))
                pdf.drawString(20,x-20, '{}'.format(ato.texto))
            #for nome,idade in lista.items():
                #x -= 20
                #pdf.drawString(247,x, '{} : {}'.format(nome,idade))
            #pdf.setTitle(str(id))
            pdf.setFont("Helvetica-Oblique", 14)
            #pdf.setFont("Helvetica-Bold", 12)
            #pdf.drawString(245,724, str(id))
            pdf.save()
            
        return super().response_change(request, obj)        


class TipoAtoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Ato, AtoAdmin)
admin.site.register(SetorOriginario, SetorOriginarioAdmin)
admin.site.register(Assunto, AssuntoAdmin)
admin.site.register(Publicacao, PublicacaoAdmin)
admin.site.register(TipoAto, TipoAtoAdmin)
admin.site.register(AssuntoSecundario, AssuntoSecundarioAdmin)
admin.site.site_header = 'Gestor de Atos - DPE/PR'
