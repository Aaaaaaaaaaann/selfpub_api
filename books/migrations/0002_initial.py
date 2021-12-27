# Generated by Django 4.0 on 2021-12-26 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='books',
                to='users.user',
            ),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='genre_books',
                to='books.genre',
            ),
        ),
    ]