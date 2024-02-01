from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthentication

from core.models import Recipe
from reciep  import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage reciepe APISL"""
    serializer_class =serializers.ReciepeSerializer
    queryset=Recipe.objects.all()
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthentication]

    def get_quersyset(self):
        """Retrieve reciepe for authenticated users"""
        return self.queryset.filter(users=self.request.user
                                    ).order_by('id')
