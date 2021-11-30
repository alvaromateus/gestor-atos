from rest_framework import serializers
from ato import models


class AtoSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Ato
        fields = '__all__'

class SetorSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SetorOriginario
        fields = '__all__'
        #fields=('id','numero','ano')

## Assuntos principais
class AssuntoSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Assunto
        fields = '__all__'
        #fields=('id','numero','ano')

## Assuntos secundarios
class AssuntoSecSerializers(serializers.ModelSerializer): 
    class Meta:
        model = models.AssuntoSecundario
        fields = '__all__'
        #fields=('id','numero','ano')
