from rest_framework import viewsets
from ato.api import serializers
from ato import models

class AtoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AtoSerializers
    queryset = models.Ato.objects.all()

class SetorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SetorSerializers
    queryset = models.SetorOriginario.objects.all()

class AssuntoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AssuntoSerializers
    queryset = models.Assunto.objects.all()

class AssuntoSecViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AssuntoSecSerializers
    queryset = models.AssuntoSecundario.objects.all()
    