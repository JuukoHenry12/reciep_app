from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from reciep.serializers import ReciepeSerializer
from decimal import Decimal

RECIPES_URL=reverse('recipe:recipe-list')

def create_recipe(user,**params):
    """Create and return sample recipe"""
    defualt={
        'title':'Sample recipe title',
        'time_miutes':22,
        'price':Decimal('5.5'),
        'decription':'Sample description',
        'link':'http://example.com/recipe.pdf'
    }

    defualt.update(params)

    recipe=Recipe.objects.create(user=user,**defualt)

    return recipe

class PublicRecipeAPITests(TestCase):
    """Test unathoricated API requests"""

    def setUp(self):
        self.client=APIClient()

    def test_auth_require(self):
        """Test auth is required  to call API"""

        res=self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code.status.HTTP_401_UNauthorized)

class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.user=get_user_model.objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticated(self.user)


    def test_retrieve_recipes(self):
        """Test retrieving alist of recipes"""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.all().order_by(
          '-id'
        )

        serializer=ReciepeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipe is limited to authenticated user"""
        other_user=get_user_model.create_user(
            'other@example.com',
            'password123'
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)
        
        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.filter(user=self.user)

        serializer=ReciepeSerializer(recipes,many=True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)

        self.assertEqual(res.data,serializer.data)