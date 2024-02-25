from django.shortcuts import render

# Create your views here.
from rest_framework import (viewsets,mixins)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (Recipe,Tag)
from reciep  import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage reciepe APISL"""
    serializer_class =serializers.RecipesDetailSerializer
    queryset=Recipe.objects.all()
    authentication_classes=[TokenAuthentication]
    permission_classes=[ IsAuthenticated]
 
    def get_quersyset(self):
        """Retrieve reciepe for authenticated users"""
        return self.queryset.filter(users=self.request.user).order_by('id')


    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        
        return self.serializer_class
    
    def perform_create(self,serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)

class TagViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """Manage tags in the database"""
    serializer_class =serializers.TagSerializer
    queryset=Tag.objects.all()
    authenitcation_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')