from django.db import models

def documento_file_name(instance, filename):    
    ext = filename.split('.')[-1]    
    return str(instance.numero)+"-"+str(instance.ano) + "." + ext

class Ato(models.Model):
    STATUS_VIGENTE = 0
    STATUS_REVOGADA = 1
    STATUS_REVOGADA = 2

    LISTA_STATUS = (
        (STATUS_VIGENTE, u'Vigente'),
        (STATUS_REVOGADA, u'Revogada'),
        (STATUS_REVOGADA, u'Sem efeito'),
    )

    TIPO_RESOLUCAO = 0
    TIPO_PORTARIA = 1
    TIPO_EDITAL = 2
    TIPO_DELIBERACAO = 3
    TIPO_NORMATIVA = 4

    LISTA_TIPO = (
        (TIPO_RESOLUCAO, u'Resolução'),
        (TIPO_PORTARIA, u'Portaria'),
        (TIPO_EDITAL, u'Edital'),
        (TIPO_DELIBERACAO, u'Deliberação'),
        (TIPO_NORMATIVA, u'Instrução Normativa'),
    )

    numero = models.IntegerField('Número', blank=False)
    ano = models.IntegerField('Ano', blank=False)
    tipo = models.PositiveSmallIntegerField(choices=LISTA_TIPO, blank=False)    
    assuntos = models.ManyToManyField('Assunto', blank=False)
    setor_originario = models.ForeignKey('SetorOriginario', blank=False, default=None, on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(choices=LISTA_STATUS, blank=False)
    texto = models.TextField('Texto documento', blank=True, null=True, default=None)    
    arquivo = models.FileField(verbose_name='Arquivo', upload_to=documento_file_name, null=True, blank=False, default=None)

    class Meta:
        verbose_name = u'Ato'
        verbose_name_plural = u'Documentos emitidos'
        ordering = ['ano']
    
    def __str__(self):
        return str(self.numero) + " / " + str(self.ano)
        
class SetorOriginario(models.Model):
    nome = models.CharField('Nome', max_length=40, blank=True, null=True, default=None)    

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
