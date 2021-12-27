from uuid import uuid4

from django.db import models
from rest_framework.fields import UUIDField
from rest_framework.serializers import ModelSerializer


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class BaseSerializer(ModelSerializer):
    id = UUIDField(read_only=True)
