from rest_framework import serializers
from ato import models


class AtoSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Ato
        fields = '__all__'