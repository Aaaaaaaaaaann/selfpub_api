from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

from shared.mixins import BaseModel


class User(BaseModel, AbstractUser):
    full_name = models.CharField(max_length=512)
    birth_year = models.PositiveSmallIntegerField(null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=256, null=True)

    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'


class Comment(BaseModel):
    author = models.ForeignKey('users.User', on_delete=CASCADE)
    book = models.ForeignKey(
        'books.Book', on_delete=CASCADE, related_name='comments'
    )
    created = models.DateTimeField(default=timezone.now, editable=False)
    text = models.TextField()

    class Meta:
        db_table = 'comments'
