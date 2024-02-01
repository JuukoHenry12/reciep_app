from core.models import Recipe
from rest_framework import serializers

class ReciepeSerializer(serializers.ModelSerializer):
    class Meta:
        fields= ['id','title','time_minute','price','link']
        read_only_fields=['id']