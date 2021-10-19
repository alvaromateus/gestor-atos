from celery import shared_task

@shared_task
def atualiza_status_atos():
    mensagem = "Teste"
    print("teste")
    return '{} Teste'.format(mensagem)