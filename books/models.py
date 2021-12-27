from django.db import models
from django.utils import timezone

from shared.mixins import BaseModel


class Genre(BaseModel):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        db_table = 'genres'

    def __str__(self) -> str:
        return self.name


class Book(BaseModel):
    title = models.TextField()
    year = models.PositiveSmallIntegerField()
    author = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='books', null=True
    )
    genre = models.ForeignKey(
        'books.Genre',
        on_delete=models.CASCADE,
        related_name='genre_books',
        null=True,
    )
    pub_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'books'
