# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip
from celery import shared_task
from celery.utils.log import get_task_logger
from ato.models import Ato
from datetime import date
from reportlab.pdfgen import canvas

logger = get_task_logger(__name__)

@shared_task
def atualiza_status_atos():
    atos = Ato.objects.filter(status__in=[0,2,3]).exclude(data_final=None)
    count = 0
    hoje = date.today()
    for ato in atos:
        if ato.data_final < hoje:
            temp = Ato.objects.get(id=ato.id)
            temp.status = 5
            temp.save()
            count += 1
    
    if count > 0:
        return '{} atos definidos com status Exaurido'.format(str(count))
    else:
        return 'Sem atos exauridos'

@shared_task
def gera_publicacao():
    lista = {'Rafaela': '19', 'Jose': '15', 'Maria': '22','Eduardo':'24'}
    try:
        nome_pdf = 'Diário número X'
        pdf = canvas.Canvas('media/{}.pdf'.format(nome_pdf))
        x = 720
        for nome,idade in lista.items():
            x -= 20
            pdf.drawString(247,x, '{} : {}'.format(nome,idade))
        pdf.setTitle(nome_pdf)
        pdf.setFont("Helvetica-Oblique", 14)
        pdf.drawString(245,750, 'Lista de Convidados')
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(245,724, 'Nome e idade')
        pdf.save()
        return '{}.pdf criado com sucesso!'.format(nome_pdf)
    except:
        return 'Erro ao gerar {}.pdf'.format(nome_pdf)