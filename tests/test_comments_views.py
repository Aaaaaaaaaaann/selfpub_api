from django.db.models import Q
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from books.models import Book
from users.models import User


class TestComments(APITestCase):
    fixtures = ['user.json', 'genre.json', 'book.json', 'comment.json']

    def setUp(self):
        self.author = User.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.author)
        self.book = Book.objects.first()
        self.url = f'/api/books/{self.book.id}/comments/'

    def test_create(self):
        data = {'text': 'Ну такое.'}
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']
        assert response.data['author']['id'] == str(self.author.id)


class TestComment(APITestCase):
    fixtures = ['user.json', 'genre.json', 'book.json', 'comment.json']

    def setUp(self):
        self.author = User.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.author)
        self.book = Book.objects.first()
        self.comment = self.book.comments.first()
        self.url = f'/api/books/{self.book.id}/comments/{self.comment.id}/'

    def test_cant_update_of_another_user(self):
        data = {'text': 'Книга супер.'}
        another_user = User.objects.filter(~Q(email=self.author.email)).first()
        self.client.force_authenticate(user=another_user)
        response = self.client.put(self.url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_cant_dupdate_as_anonym(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete(self):
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

