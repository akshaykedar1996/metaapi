from rest_framework import serializers
from .models import ClientDetail

class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDetail
        fields = '__all__'  # This will include all fields in the model
