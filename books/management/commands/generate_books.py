from typing import Any, Optional

from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)
from django.db import Error

from books.services.datagens import BooksGenerator


class Command(BaseCommand):
    help = 'Fill database fake data.'
    arguments = ('authors', 'books', 'comments', 'libraries')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--authors', type=int, dest='authors')
        parser.add_argument('--books', type=int, dest='books')
        parser.add_argument('--comments', type=int, dest='comments')
        parser.add_argument('--libs', type=int, dest='libraries')

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        opts = {k: v for k, v in options.items() if k in self.arguments and v}
        gen = BooksGenerator(**opts)
        try:
            gen.generate()
        except Error as e:
            raise CommandError(f'Failed to generate data, {e}.')
        else:
            self.stdout.write(self.style.SUCCESS('Done.'))
