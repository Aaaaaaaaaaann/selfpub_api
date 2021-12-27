from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from books.models import Book, Genre
from books.serializers import (
    BookCreateSerializer,
    BookReadSerializer,
    BookUpdateSerializer,
    GenreSerializer,
)
from shared.permissions import IsAuthor
from users.models import Comment
from users.serializers import (
    CommentCreateUpdateSerializer,
    CommentReadSerializer,
)


class GenreViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Book.objects.all()
    serializer_class = BookReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        book = Book.objects.create(
            author=request.user,
            title=data['title'],
            year=data['year'],
            genre_id=data['genre'],
        )
        return Response(
            BookReadSerializer(book).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = BookUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        book = self.get_object()
        for filed, value in data.items():
            setattr(book, filed, value)
        book.save()

        return Response(BookReadSerializer(book).data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorBooks(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReadSerializer

    def get_queryset(self, *args, **kwargs):
        return Book.objects.filter(author_id=self.kwargs['author_id'])


class CommentsView(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentReadSerializer

    def get_queryset(self, *args, **kwargs):
        return Comment.objects.filter(book_id=self.kwargs['book_id'])

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        comment = Comment.objects.create(
            author=request.user,
            book_id=kwargs['book_id'],
            text=data['text'],
        )
        return Response(
            CommentReadSerializer(comment).data, status=status.HTTP_201_CREATED
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        serializer = CommentCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        comment = self.get_object()
        comment.text = data['text']
        comment.save()

        return Response(CommentReadSerializer(comment).data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
