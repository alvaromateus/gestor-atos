from rest_framework import viewsets
from ato.api import serializers
from ato import models

class AtoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AtoSerializers
    queryset = models.Ato.objects.all()