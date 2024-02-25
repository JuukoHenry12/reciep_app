"""
Testing tags
"""
from django.contrib.auth import  get_user_model
from django.test import TestCase
from django.urls import reverse
from restframework.test import APIClient
from restframework import status
from core.models import Tag
from serializers import TagSerializer

TAG_URL=reverse('recipe:list')

def create_user(email="example@gmail.com",password="test123"):

    """creating a test user"""

    return get_user_model().objects.create_user(email,password)

class PublicTagTest(TestCase):
    """test unathenticated user"""
    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        """test auth is required for retrieving tags"""
        res=self.client.get(TAG_URL)
        self.assertEquals(res.status_code,status.HTTP_401_UNANTHORIZED)


class PrivateTagsTests(TestCase):

    def setUp(self):
        self.user=create_user()
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Tests retrieving a list of tags"""
        Tag.objects.create(user=self.user,name='Vegans')
        Tag.objects.create(user=self.user,name='Dessert')
        res=self.client.get(TAG_URL)
    
        tags=Tag.objects.all().order_by('-name')
        serializer=TagSerializer(tags,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user"""
        user2=create_user(email='user2@example.com')
        Tag.objects.create(user=user2,name='Fruity')
        tag=Tag.objects.create(user=self.user,name='Comfort food')
        res=self.client.get(TAG_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual([res.data][0]['name'],tag.name)
        self.assertEqual(res.data[0]['id'],tag.id)
