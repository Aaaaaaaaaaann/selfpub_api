from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import (
    Serializer,
    SerializerMethodField,
    StringRelatedField,
    UUIDField,
)

from books.models import Book, Genre
from shared.mixins import BaseSerializer
from users.serializers import AuthorShortReadSerializer


class GenreSerializer(BaseSerializer):
    books_count = SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'name', 'books_count')

    def get_books_count(self, instance):
        return Book.objects.filter(genre=instance).count()


class BookReadSerializer(BaseSerializer):
    id = UUIDField()
    author = AuthorShortReadSerializer()
    genre = StringRelatedField()

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'year',
            'genre',
            'pub_date',
        )


class BookCreateSerializer(Serializer):
    title = CharField()
    year = IntegerField()
    genre = CharField()

    def validate_genre(self, value):
        try:
            genre = Genre.objects.get(name=value)
        except Genre.DoesNotExist:
            raise ValidationError('No such a genre.')
        return genre.id


class BookUpdateSerializer(BookCreateSerializer):
    name = CharField(required=False)
    year = IntegerField(required=False)
    genre = CharField(required=False)
