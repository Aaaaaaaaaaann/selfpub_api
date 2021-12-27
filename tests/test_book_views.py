from django.db.models import Q
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User


class TestBooks(APITestCase):
    fixtures = ['user.json', 'genre.json', 'book.json']

    def setUp(self, *args):
        self.author = User.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.author)
        self.url = '/api/books/'

    def test_cant_get_as_anonym(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create(self):
        data = {
            'title': 'Название',
            'year': 2021,
            'genre': 'бизнес',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert response.data['author']['id'] == str(self.author.id)
    
    def test_cant_create_with_non_existent_genre(self):
        data = {
            'name': 'Название',
            'year': 2021,
            'genre': 'жанр, которого у нас нет',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestBook(APITestCase):
    fixtures = ['user.json', 'genre.json', 'book.json']

    def setUp(self, *args):
        self.author = User.objects.first()
        self.client = APIClient()
        self.book = self.author.books.first()
        self.url = f'/api/books/{self.book.id}/'

    def test_cant_update_as_another_user(self):
        another_user = User.objects.filter(~Q(email=self.author.email)).first()
        data = {'title': 'Другое название'}
        self.client.force_authenticate(user=another_user)
        response = self.client.patch(self.url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_cnat_delete_as_another_user(self):
        another_user = User.objects.filter(~Q(email=self.author.email)).first()
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
