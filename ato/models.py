from django.db import models

def documento_file_name(instance, filename):
    import uuid

    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    return '/'.join(['atos', str(instance.numero)+"-"+str(instance.ano), filename])

class Ato(models.Model):
    STATUS_VIGENTE = 0
    STATUS_REVOGADA = 1
    STATUS_REVOGADA = 2

    LISTA_STATUS = (
        (STATUS_VIGENTE, u'Vigente'),
        (STATUS_REVOGADA, u'Revogada'),
        (STATUS_REVOGADA, u'Sem efeito'),
    )

    numero = models.IntegerField('Número', blank=False)
    ano = models.IntegerField('Ano', blank=False)
    tipo = models.ForeignKey('Tipo', blank=False, default=None, on_delete=models.PROTECT)
    assuntos = models.ManyToManyField('Assunto', blank=False)
    setor_originario = models.ForeignKey('SetorOriginario', blank=False, default=None, on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(choices=LISTA_STATUS, blank=True, null=True, default=None)
    arquivo = models.FileField(verbose_name='Arquivo', upload_to=documento_file_name, null=True, blank=True, default=None)

    class Meta:
        verbose_name = u'Ato'
        verbose_name_plural = u'Atos'
        ordering = ['ano']
    
    def __str__(self):
        return str(self.numero) + " / " + str(self.ano)

class Tipo(models.Model):
    descricao = models.TextField('Descrição', max_length=25, blank=True, null=True, default=None)

    def __str__(self):
        return self.descricao

    class Meta:        
        ordering = ['descricao']

class SetorOriginario(models.Model):
    nome = models.TextField('Nome', max_length=40, blank=True, null=True, default=None)    

    class Meta:        
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Assunto(models.Model):
    nome = models.CharField(max_length=200)    

    class Meta:        
        ordering = ['nome']

    def __str__(self):
        return self.nome
