"""
Tests for Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from decimal import Decimal

class ModelTest(TestCase):
    """Test models"""
    def test_create_user_with_email_successful(self):
        """Test cereting a user with an email is successful"""
        email='test@example.com'
        password='testpass123'

        user=get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ['test@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.com','TEST3@example.com'],
            ['test4@example.com','test4@example.com'],
        ]

        for email,expected in sample_emails:
            user=get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user with"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        """Testing creating a superuser"""
        user=get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """"Testing creating a recipe successful"""

        user = get_user_model.objects.create_user(
          "test@exmaple.com",
          "test@123456"
        )

        recipe = model.Recipe.objects.create(
            user=user,
            title='sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description="sample recipe description"
        )

        self.assertEqual(str(recipe),recipe.title)