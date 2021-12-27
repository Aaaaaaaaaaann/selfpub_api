from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from books.views import (
    AuthorBooks,
    BookViewSet,
    CommentsView,
    CommentView,
    GenreViewSet,
)

books_router = DefaultRouter()

books_router.register('genres', GenreViewSet)
books_router.register('books', BookViewSet)

books_urls = [
    path('api/', include(books_router.urls)),
    path('api/books/<uuid:book_id>/comments/', CommentsView.as_view()),
    path(
        'api/books/<uuid:book_id>/comments/<uuid:id>/', CommentView.as_view()
    ),
    path('api/authors/<uuid:author_id>/books/', AuthorBooks.as_view()),
]
