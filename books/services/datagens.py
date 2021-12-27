import json
from datetime import date
from functools import lru_cache
from os import path
from random import choice, randint
from typing import Any, Final, Optional, Union

from django.db import transaction
from django.db.models.query import QuerySet
from mimesis import Address, Person, Text
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider

from books.models import Book, Genre
from libraries.models import Library
from users.models import Comment, User


class GenreProvider(BaseDataProvider):
    """The class extends mimesis behaviour to generate
    believable book genres names.
    """

    name = 'genres'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._data_file = path.join('data', f'{self.name}.json')
        self._load_datafile(self._data_file)
        self._sample_name: Final[str] = 'genre'

    def genre(self) -> str:
        return self._choice_from(self.name)

    @lru_cache(maxsize=None)
    def _load_datafile(self, file_path: str) -> None:
        with open(file_path) as file:
            self._data = json.load(file)

    def _choice_from(self, key: str) -> str:
        data: list[str] = self.extract([key])
        return self.random.choice(data)


class BooksGenerator:
    """The class fills database with sampes data."""

    def __init__(
        self,
        *,
        authors: int = 500,
        books: int = 5,
        comments: int = 5,
        libraries: int = 0,
    ) -> None:
        self._authors_number = authors
        self._books_number = books
        self._comments_number = comments
        self._libraries_number = libraries
        # TODO: Allow other locals afret GenreProvider extending.
        self._locale = Locale.RU

        self._authors: Optional[list[User]] = None
        self._genres: Optional[Union[list[Genre], 'QuerySet[User]']] = None
        self._books: Optional[list[Book]] = None

    @transaction.atomic
    def generate(self) -> None:
        self._authors = self._create_authors()
        self._genres = self._get_or_create_genres()
        self._books = self._create_books()
        self._create_comments()
        self._create_libraries()

    def _create_authors(self) -> list[User]:
        person = Person(self._locale)
        current_year = date.today().year
        users = [
            User(
                full_name=person.full_name(),
                email=person.email(),
                birth_year=(current_year - person.age()),
            )
            for _ in range(self._authors_number)
        ]
        return User.objects.bulk_create(users)

    def _get_or_create_genres(self) -> Union[list[Genre], 'QuerySet[User]']:
        if Genre.objects.count() > 0:
            return Genre.objects.all()

        genre = GenreProvider()
        names = {genre.genre() for _ in range(25)}
        genres = [Genre(name=name) for name in names]
        return Genre.objects.bulk_create(genres)

    def _create_books(self) -> list[Book]:
        text = Text(locale=self._locale)
        books = []
        for author in self._authors:
            genre = choice(self._genres)
            for _ in range(self._books_number):
                books.append(
                    Book(
                        author=author,
                        genre=genre,
                        title=text.quote().rstrip('.'),
                        year=(author.birth_year + randint(16, 60)),
                    )
                )
        return Book.objects.bulk_create(books)

    def _create_comments(self) -> None:
        text = Text(locale=self._locale)
        comments = []
        for book in self._books:
            for _ in range(self._comments_number):
                comment_author = choice(self._authors)
                comments.append(
                    Comment(
                        author=comment_author,
                        book=book,
                        text=text.title(),
                    )
                )
        Comment.objects.bulk_create(comments)

    def _create_libraries(self) -> None:
        address = Address(locale=self._locale)
        libraries = [
            Library(
                name=f'Библиотека № {randint(1, 1000)}',
                address=address.address(),
                timetable=f'Ежедневно с {randint(7, 11)} до {17, 22}.',
            )
        ]
        Library.objects.bulk_create(libraries)
