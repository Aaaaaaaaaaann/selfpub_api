from django.db import models

from books.models import BaseModel


class Library(BaseModel):
    name = models.CharField(max_length=512)
    address = models.TextField(null=True)
    timetable = models.TextField(null=True)

    class Meta:
        db_table = 'libraries'
