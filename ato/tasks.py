# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def atualiza_status_atos():
    resultado = 1+1
    mensagem = "Teste"
    print("teste")
    return '{} Teste {}'.format(mensagem, str(resultado))