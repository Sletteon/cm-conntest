from rest_framework import serializers
from .models import Bejegyzes

class BejegyzesSerializer(serializers.ModelSerializer):


    class Meta:
        model = Bejegyzes
        fields = '__all__'