from .models import Assunto, AssuntoSecundario, Ato
from django.shortcuts import HttpResponse
import json

# chamada ajax para retornar lista de assuntos secundários
def get_assuntos_secundarios(request):
    if request.is_ajax():
        assuntos = request.GET.get('ids[]', '')
        assuntos_secundarios = AssuntoSecundario.objects.filter(assuntos__in=assuntos)
        assunto_dict = {}
        for assunto_secundario in assuntos_secundarios:
            assunto_dict[assunto_secundario.pk] = assunto_secundario.nome        
        return HttpResponse(json.dumps(assunto_dict))

# chamada ajax para retornar lista de assuntos secundários
def get_numero_documento(request):
    if request.is_ajax():
        tipo = request.GET.get('tipo', '')
        ano = request.GET.get('ano', '')
        setor_originario = request.GET.get('setor', '')
        numero_documento = 0
        try:
            documento = Ato.objects.filter(tipo=tipo, ano=ano, setor_originario=setor_originario).order_by('-numero')[0]        
            numero_documento = documento.numero+1
        except:
            numero_documento = 1
        
        return HttpResponse(numero_documento)
