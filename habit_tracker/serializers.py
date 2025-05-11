from rest_framework import serializers
from habit_tracker.models import Habit
from habit_tracker.validators import RewardOrRelatedValidator, ExecutionTimeValidator, PleasantRelatedValidator, \
    PleasantHabitValidator, FrequencyValidator, RelatedPublicValidator, RelatedOwnerValidator
from datetime import timedelta


class RelatedHabitSerializer(serializers.ModelSerializer):
    """ Класс сериализатора к модели "Привычки" (только для чтения). """

    class Meta:
        """Класс для изменения поведения полей сериализатора связанной привычки модели "Привычки"."""
        model = Habit
        fields = '__all__'


class DurationFieldInSeconds(serializers.DurationField):
    """ Класс сериализатора для поля длительности. """
    def to_representation(self, value):
        """Метод для вывода значения поля в читаемом для пользователя виде."""
        if not value:
            return None
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def to_internal_value(self, data):
        """Метод для вывода времени в виде интервала."""
        try:
            parts = list(map(int, data.split(':')))
            if len(parts) == 3:
                return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
            elif len(parts) == 2:
                return timedelta(minutes=parts[0], seconds=parts[1])
            raise serializers.ValidationError('Недопустимый формат времени. Используйте "ЧЧ:ММ:СС" или "ММ:СС".')
        except (ValueError, TypeError):
            raise serializers.ValidationError("Недопустимый формат времени. Используйте числа, разделенные двоеточием.")


class HabitSerializer(serializers.ModelSerializer):
    """ Класс сериализатора с ограниченным доступом к модели "Привычки" (только для чтения). """
    execution_time = DurationFieldInSeconds(
        help_text="Формат: ЧЧ:ММ:СС или MM:SS (например: 00:02:00 в течение 2 минут)"
    )
    related_habit = RelatedHabitSerializer(read_only=True)
    related_habit_id = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        source='related_habit',
        write_only=True,
        allow_null=True,
        default=None
    )

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Привычки"."""

        model = Habit
        fields = [
            'id', 'name', 'place', 'date_completion', 'action', 'is_pleasant',
            'periodicity', 'award', 'execution_time', 'is_public', 'owner',
            'related_habit', 'related_habit_id'
        ]
        validators = [
            RewardOrRelatedValidator('is_pleasant', 'related_habit', 'award'),
            ExecutionTimeValidator('execution_time'),
            PleasantRelatedValidator('related_habit'),
            PleasantHabitValidator('is_pleasant', 'award', 'related_habit'),
            FrequencyValidator('periodicity'),
            RelatedPublicValidator('related_habit', 'is_public'),
            RelatedOwnerValidator('related_habit', 'owner')
        ]
