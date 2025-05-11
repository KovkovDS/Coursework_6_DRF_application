from rest_framework import generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from habit_tracker.models import Habit
from habit_tracker.paginators import HabitsPaginator
from habit_tracker.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitsListAPIView(generics.ListAPIView):
    """Класс представления вида Generic для эндпоинта списка привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitsPaginator

    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Привычки"."""

        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(Q(owner=user) | Q(is_public=True)).order_by('id')
        else:
            return Habit.objects.filter(is_public=True).order_by('id')


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Класс представления вида Generic для эндпоинта просмотра привычки."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс представления вида Generic для эндпоинта создания привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Привычки"."""

        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Класс представления вида Generic для эндпоинта изменения привычки."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Класс представления вида Generic для эндпоинта удаления привычки."""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
