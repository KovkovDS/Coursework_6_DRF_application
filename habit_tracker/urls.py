from django.urls import path
from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import (
    HabitCreateAPIView,
    HabitsListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
)


app_name = HabitTrackerConfig.name

urlpatterns = [
    path("habits/", HabitsListAPIView.as_view(), name="habits"),
    path("habit/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit"),
    path("habit/new/", HabitCreateAPIView.as_view(), name="adding_habit"),
    path("habit/<int:pk>/update/", HabitUpdateAPIView.as_view(), name="update_habit"),
    path("habit/<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="delete_habit"),
]
