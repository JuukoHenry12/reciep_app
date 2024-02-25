from core.models import Recipe
from rest_framework import serializers
from core.models import Tag
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""
    class Meta:
        fields= ['id','title','time_minute','price','link']
        read_only_fields=['id']


class RecipesDetailSerializer(RecipeSerializer):
    """serial for recipe description"""
    class Meta(RecipeSerializer.Meta):
         fields = RecipeSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model=Tag
        fields=['id','name']
        read_only_fields=['id']

        