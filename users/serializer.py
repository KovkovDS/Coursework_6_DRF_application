from rest_framework import serializers
from users.models import User


class ProfileUserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователя."""

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Пользователь"."""

        model = User
        fields = ['avatar', 'email', 'telegram_nickname', 'tg_chat_id', 'city']


class ProfileSerializer(serializers.ModelSerializer):
    """Класс сериализатора с ограниченным доступом к модели пользователя."""

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Пользователь"."""

        model = User
        fields = ["avatar", "email", "city"]


class CreateProfileSerializer(serializers.ModelSerializer):
    """Класс сериализатора для создания пользователя с базовым доступом."""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Пользователь"."""

        model = User
        fields = ["avatar", "email", "phone_number", "city", "password"]
