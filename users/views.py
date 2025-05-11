from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.permissions import IsUserOwner
from users.serializer import (
    ProfileSerializer,
    CreateProfileSerializer,
    ProfileUserSerializer,
)


class ProfilesListAPIView(generics.ListAPIView):
    """Класс представления вида Generic для эндпоинта списка пользователей."""

    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Класс представления вида Generic для эндпоинта просмотра профиля пользователя."""

    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Метод получения сериализатора в соответствии с запросом."""

        if (
            self.request.method == "GET"
            and self.get_object() != self.request.user
            or self.request.user.is_superuser is False
        ):
            return ProfileSerializer
        if self.request.user.is_superuser:
            return ProfileUserSerializer
        return ProfileUserSerializer


class ProfileCreateAPIView(generics.CreateAPIView):
    """Класс представления вида Generic для эндпоинта создания пользователя."""

    serializer_class = CreateProfileSerializer

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Пользователя"."""

        user = serializer.save()
        user.set_password(user.password)
        user.save()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """Класс представления вида Generic для эндпоинта редактирования профиля пользователя."""

    serializer_class = ProfileUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class ProfileDestroyAPIView(generics.DestroyAPIView):
    """Класс представления вида Generic для эндпоинта удаления профиля пользователя."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]
