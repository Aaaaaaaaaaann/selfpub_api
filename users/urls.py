from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from users.views import AuthorViewSet

authors_router = DefaultRouter()

authors_router.register('authors', AuthorViewSet)

authors_urls = [
    path('api/', include(authors_router.urls)),
]