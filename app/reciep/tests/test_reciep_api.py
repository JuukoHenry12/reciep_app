from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe  # Corrected import
from decimal import Decimal  # No correction needed, this import seems fine
from serializers import RecipeSerializer

RECIPES_URL=reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """create and return recipe"""
    return reverse('recipe:recipe-detail',args=[recipe_id])

def create_recipe(user,**params):
    """create and return sample recipe"""
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

def create_user(**params):
    """create and return a new user"""
    return get_user_model.objects.create_user(**params)


class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.user = create_user(
          email = 'user@example.com',
          password='test123'
        )
        self.user=get_user_model.objects.create_user(
            'user@example.com',
            'testpass123'
        )

        self.client.force_authenticate(self.user)


    def test_retrieve_recipes(self):
        """Test retrieving alist of recipes""" 
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res=self.client.get(RECIPES_URL)
        recipes=Recipe.objects.all().order_by(
          '-id'
        )
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipe is limited to authenticated user"""
        other_user=create_user(
           email='other@example.com',
           password='password123'
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)
        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.filter(user=self.user)
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
    
    def test_get_recipe_detail(self):
        """Test get recipe details"""
        recipe=create_recipe(user=self.user)
        url=detail_url(recipe.id)
        res=self.client.get(url)

        serializer=RecipeSerializer(recipe)

        self.assertEqual(res.data,serializer.data)


    def test_create_recipe(self):
        """Test creating a recipe"""
        payload={
            'title':'sample recipe',
            'time_minutes':30,
            'price':Decimal('5.99')
        }

        res=self.client.post(RECIPES_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe=Recipe.objects.get(id=res.data['id'])

        for k,v in payload.items():
            self.assertEqual(getattr(recipe,k),v)
            self.assertEqual(recipe.user,self.user)


    def test_partial_update(self):
        """Test partial update a recipe"""
        original_link='https://example.com/recipe.pdf'

        recipe=create_recipe(
            user=self.user,
            title='sample recipe title',
            link=original_link
        )

        payload = {
            'title':'New recipe title'
        }

        url =detail_url(recipe.id)

        res=self.client.patch(url,payload)

        self.assertEqual(res.status_code,status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.title,payload)
        
        self.assertEqual(recipe.link,original_link)
    
    def test_full_update(self):
        """Test full update of recipe"""
        recipe =create_recipe(
            user=self.user,
            title='sample recipe title',
            link='https://example.com/recipe.pdf',
            description='sample recipe description'
        )

        payload={
            'title':'New recipe title',
            'link':'https://example.com/new-recipe.pdf',
            'decription':'New recipe description',
            'time_minute':10,
            'price':Decimal('2.05')
        }

        url =detail_url(recipe.id)
        res=self.client.put(url,payload)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k,v in payload.items():
            self.assertEqual(getattr(recipe,k),v)
        self.assertEqual(recipe.user,self.user)
    
    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error"""
        new_user=create_user(
          email ='user2@exmaple.com',
          password='test123!@#'                   
        )
        recipe =create_recipe(user=self.user)
        payload = {
            'user':new_user.id
        }
        url =detail_url(recipe.id)
        self.client.patch(url,payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user,self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe successful"""

        recipe=create_recipe(user=self.user)
        url=detail_url(recipe.id)
        res=self.client.delete(url)
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
    
    def test_recipe_other_user_recipe_error(self):
        """Test try delete another users recipe gives error"""
        new_user=create_recipe(
            email='user2@xample.com',
            password='test133'
        )
        recipe = create_recipe(user=new_user)
        url=detail_url(recipe.id)
        res=self.client.delete(url)
        self.assertEqual(res.status_code,status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())