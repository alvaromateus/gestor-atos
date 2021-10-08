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
    assuntos_secundarios = models.ManyToManyField('AssuntoSecundario', blank=True, null=True)

    setor_originario = models.ForeignKey('SetorOriginario', blank=False, default=None, on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(choices=LISTA_STATUS, blank=False)
    texto = models.TextField('Texto documento', blank=True, null=True, default=None)    
    
    arquivo = models.FileField(verbose_name='Extrato Dioe', upload_to=documento_file_name, null=True, blank=False, default=None)
    arquivo_02 = models.FileField(verbose_name='PDF Pesquisável', upload_to=documento_file_name, null=True, blank=True, default=None)
    arquivo_03 = models.FileField(verbose_name='Arquivo editável (Word ou similar)', upload_to=documento_file_name, null=True, blank=True, default=None)
    
    documento_alterado = models.ForeignKey('Ato', blank=True, null=True, default=None, related_name="atos_alterados", 
        verbose_name='Este documento altera outro? Caso positivo selecione o documento alterado', on_delete=models.PROTECT)
    
    documento_revogado = models.ForeignKey('Ato', blank=True, null=True, default=None, related_name="atos_revogados", 
        verbose_name='Este documento revoga outro? Caso positivo selecione o documento revogado', on_delete=models.PROTECT)

    atos_vinculados = models.ManyToManyField("self", verbose_name='Atos relacionados', null=True, blank=True, default=None)

    data_inicial = models.DateField(null=True, blank=True, default=None, verbose_name='Data do início da vigência do ato')
    data_final = models.DateField(null=True, blank=True, default=None, verbose_name='Data do final da vigência do ato')

    class Meta:
        verbose_name = u'Ato'
        verbose_name_plural = u'Documentos emitidos'
        ordering = ['ano']
    
    def __str__(self):
        return str(self.numero) + " / " + str(self.ano)
        
class SetorOriginario(models.Model):
    nome = models.CharField('nome do setor originário', max_length=40, blank=True, null=True, default=None)    

    class Meta:        
        ordering = ['nome']
        verbose_name = u'Setor Originário'
        verbose_name_plural = u'Setores Originários'

    def __str__(self):
        return self.nome

class Assunto(models.Model):
    nome = models.CharField(max_length=200)
    assuntos_secundarios = models.ManyToManyField('AssuntoSecundario', blank=True, null=True)

    class Meta:        
        ordering = ['nome']

    def __str__(self):
        return self.nome

class AssuntoSecundario(models.Model):
    nome = models.CharField(max_length=200)    

    class Meta:        
        verbose_name = u'Assunto Secundário'
        verbose_name_plural = u'Assuntos Secundários'
        ordering = ['nome']

    def __str__(self):
        return self.nome
