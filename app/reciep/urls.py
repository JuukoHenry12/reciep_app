"""
URL mappings for the reciepe app
"""

from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter
from reciep import views
router =DefaultRouter()
router.register('recipes',views.RecipeViewSet)
app_name='reciep'
urlpatterns=[
    path('',include(router.urls))
]