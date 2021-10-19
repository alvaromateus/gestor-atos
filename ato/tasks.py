# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip
from celery import shared_task
from celery.utils.log import get_task_logger
from ato.models import Ato
from datetime import date

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