from rest_framework.fields import CharField, EmailField, IntegerField
from rest_framework.serializers import Serializer, SerializerMethodField

from books.models import Book, Genre
from shared.mixins import BaseSerializer
from users.models import Comment, User


class AuthorFullReadSerializer(BaseSerializer):
    books_count = SerializerMethodField()
    genres = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'birth_year',
            'email',
            'books_count',
            'genres',
        )

    def get_books_count(self, instance):
        return Book.objects.filter(author=instance).count()

    def get_genres(self, instance):
        return (
            Genre.objects.filter(genre_books__author=instance)
            .values_list('name', flat=True)
            .distinct()
        )


class AuthorShortReadSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
        )


class AuthorUpdateSerializer(Serializer):
    full_name = CharField(required=False)
    birth_year = IntegerField(required=False)
    email = EmailField(required=False)


class CommentReadSerializer(BaseSerializer):
    author = AuthorShortReadSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created',
        )


class CommentCreateUpdateSerializer(Serializer):
    text = CharField()
