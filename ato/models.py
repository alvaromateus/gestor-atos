from django.db import models
from ckeditor.fields import RichTextField
from datetime import date

def documento_file_name(instance, filename):    
    ext = filename.split('.')[-1]    
    return str(instance.tipo)+"-"+str(instance.numero)+"-"+str(instance.ano)+"-"+str(instance.setor_originario.sigla) + "." + ext

def get_data_por_extenso(data):
        mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'março', 4: 'abril', 5: 'maio', 6: 'junho', 
            7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
        data_string = '{}/{}/{}'.format(data.day, data.month,data.year)        
        dia, mes, ano = data_string.split("/")
        return str(('%s de %s de %s' % (dia, mes_ext[int(mes)], ano)))

class Ato(models.Model):    
    STATUS_VIGENTE = 0
    STATUS_REVOGADO = 1
    STATUS_REVOGADO_PARCIALMENTE = 2
    STATUS_ALTERADO = 3
    STATUS_SEM_EFEITO = 4
    STATUS_EXAURIDO = 5
    STATUS_SUSPENSO = 6

    LISTA_STATUS = (
        (STATUS_VIGENTE, u'Vigente'),
        (STATUS_REVOGADO, u'Revogado'),
        (STATUS_REVOGADO_PARCIALMENTE, u'Revogado parcialmente'),
        (STATUS_ALTERADO, u'Alterado'),
        (STATUS_SEM_EFEITO, u'Sem efeito'),
        (STATUS_EXAURIDO, u'Exaurido'),
        (STATUS_SUSPENSO, u'Suspenso'),
    )

    TIPO_RESOLUCAO = 0
    TIPO_PORTARIA = 1
    TIPO_EDITAL = 2
    TIPO_DELIBERACAO = 3
    TIPO_NORMATIVA = 4

    TIPO_REVOGADO = 0
    TIPO_REVOGADO_PARCIAL = 1

    LISTA_REVOGADO = (
        (TIPO_REVOGADO, u'Revogado totalmente'),
        (TIPO_REVOGADO_PARCIAL, u'Revogado parcialmente'),
    )

    numero = models.IntegerField('nº', blank=False)
    data_documento = models.DateField(null=False, blank=False, verbose_name='Data do documento', default=date.today())
    ano = models.IntegerField('Ano', null=True, blank=True)

    setor_originario = models.ForeignKey('SetorOriginario', blank=False, default=None, on_delete=models.PROTECT)
    tipo = models.ForeignKey('TipoAto', null=True, blank=False, default=None, on_delete=models.PROTECT)
    publicacao = models.ForeignKey('Publicacao', null=True, blank=False, default=None, on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(choices=LISTA_STATUS, blank=False, default=0)

    data_suspensao = models.DateField(null=True, blank=True, default=None, verbose_name='Data da suspensão do ato')
    
    assuntos = models.ManyToManyField('Assunto', blank=False)
    assuntos_secundarios = models.ManyToManyField('AssuntoSecundario', blank=True, null=True)    
    
    texto = RichTextField('Texto documento', blank=False, null=False, default=None)  
    
    arquivo = models.FileField(verbose_name='Extrato Dioe', upload_to=documento_file_name, null=True, blank=False, default=None)
    arquivo02 = models.FileField(verbose_name='PDF Pesquisável', upload_to=documento_file_name, null=True, blank=True, default=None)
    arquivo03 = models.FileField(verbose_name='Arquivo editável (Word ou similar)', upload_to=documento_file_name, null=True, blank=True, default=None)
    
    eh_alterador = models.BooleanField('Este documento altera outro?', default=False)
    documentos_alterados = models.ManyToManyField("self", verbose_name='Documento(s) alterado(s)', null=True, blank=True, default=None)         

    eh_revogador = models.BooleanField('Este documento revoga outro?', default=False)    
    documentos_revogados = models.ManyToManyField("self", verbose_name='Documento(s) revogado(s)', null=True, blank=True, default=None)
    tipo_revogacao = models.PositiveSmallIntegerField(choices=LISTA_REVOGADO, null=True, blank=True)

    atos_vinculados = models.ManyToManyField("self", verbose_name='Outros atos relacionados', null=True, blank=True, default=None)

    data_inicial = models.DateField(null=True, blank=True, default=None, verbose_name='Data do início da vigência do ato')
    data_final = models.DateField(null=True, blank=True, default=None, verbose_name='Data do final da vigência do ato')

    class Meta:
        verbose_name = u'Ato'
        verbose_name_plural = u'Atos'
        ordering = ['ano']
        unique_together = ('ano', 'numero', 'tipo','setor_originario','status',)
    
    class Media:
        js = ("ato.js",)

    def __str__(self):        
        return '{} nº {}/{} de {} ({})'.format(self.tipo, str(self.numero), str(self.ano), get_data_por_extenso(self.data_documento), str(self.setor_originario.sigla))        

    def save(self, *args, **kwargs):                
        self.ano = '{}'.format(self.data_documento.year)
        super(Ato, self).save(*args, **kwargs)

    def atos_revogantes(self):
        if self.id:
            revogantes = Ato.objects.filter(documentos_revogados=self)
            if revogantes:
                temp = ""
                for revogante in revogantes:
                    temp = temp+str(revogante)+"\n"
            else:
                temp = "Não há"
        else:
            temp = "Não há"
        return temp

    def atos_alterantes(self):
        if self.id:
            alterantes = Ato.objects.filter(documentos_alterados=self)
            if alterantes:
                temp = ""
                for alterante in alterantes:
                    temp = temp+str(alterante)+"\n"
            else:
                temp = "Não há"
        else:
            temp = "Não há"
        return temp    

class TipoAto(models.Model):
    nome = models.CharField('nome', max_length=200)
    class Meta:        
        verbose_name = u'Tipo de ato'
        verbose_name_plural = u'Tipos de atos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    numero = models.IntegerField('Nº da Edição', blank=False, unique=True)
    data = models.DateField(null=False, blank=False, verbose_name='Data da publicação', default=date.today())

    class Meta:
        ordering =['numero']
        verbose_name = u'Publicação'
        verbose_name_plural = u'Publicações'

    def __str__(self):
        return 'Publicação nº {} de {}'.format(str(self.numero), get_data_por_extenso(self.data))

class SetorOriginario(models.Model):
    nome = models.CharField('nome do setor originário', max_length=60, blank=True, null=True, default=None)    
    sigla = models.CharField('sigla', max_length=5, blank=True, null=True, default=None)    

    class Meta:        
        ordering = ['nome']
        verbose_name = u'Setor Originário'
        verbose_name_plural = u'Setores Originários'

    def __str__(self):
        return self.nome

class Assunto(models.Model):
    nome = models.CharField('assunto principal', max_length=200)
    assuntos_secundarios = models.ManyToManyField('AssuntoSecundario', blank=True, null=True)
    class Meta:        
        ordering = ['nome']
        verbose_name = u'Assunto Principal'
        verbose_name_plural = u'Assuntos Principais'

    def __str__(self):
        return self.nome

    @property
    def get_assuntos_secundarios(self):
        return AssuntoSecundario.objects.filter(assuntos_secundarios__id=self.id)

class AssuntoSecundario(models.Model):
    nome = models.CharField('assunto secundário', max_length=200)    

    class Meta:        
        verbose_name = u'Assunto Secundário'
        verbose_name_plural = u'Assuntos Secundários'
        ordering = ['nome']

    def __str__(self):
        return self.nome