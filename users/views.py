from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.permissions import IsUserAccount
from users.models import User
from users.serializers import AuthorFullReadSerializer, AuthorUpdateSerializer


class AuthorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserAccount]
    queryset = User.objects.filter(is_active=True)
    serializer_class = AuthorFullReadSerializer

    def update(self, request, *args, **kwargs):
        serializer = AuthorUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        author = self.get_object()
        for filed, value in data.items():
            setattr(author, filed, value)
        author.save()

        return Response(AuthorFullReadSerializer(author).data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
