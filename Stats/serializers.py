
from rest_framework import serializers
from .models import *

class TopProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    value = serializers.IntegerField()

class ExportStatisticsSerializer(serializers.Serializer):
    current = serializers.DecimalField(max_digits=20, decimal_places=2)
    increase = serializers.DecimalField(max_digits=20, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

class ImportStatisticsSerializer(serializers.Serializer):
    current = serializers.DecimalField(max_digits=20, decimal_places=2)
    increase = serializers.DecimalField(max_digits=20, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)