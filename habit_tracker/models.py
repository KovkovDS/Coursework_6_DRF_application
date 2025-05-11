from datetime import timedelta
from django.db import models
from users.models import User


class Habit(models.Model):
    """ Habit model """
    name = models.CharField(max_length=200, verbose_name='Наименование привычки', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель привычки', blank=True, null=True)
    place = models.CharField(max_length=100, verbose_name='Место', blank=True, null=True)
    date_completion = models.TimeField(verbose_name='Дата начала выполнения', blank=True, null=True)
    action = models.CharField(max_length=200, verbose_name='Действие', blank=True, null=True)
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка',
                                      related_name='related_habits', blank=True, null=True)
    periodicity = models.PositiveSmallIntegerField(default=7, verbose_name="Периодичность привычки")
    award = models.CharField(max_length=100, verbose_name='Вознаграждение', blank=True, null=True)
    execution_time = models.DurationField(default=timedelta(seconds=120), verbose_name='Требуется времени')
    is_public = models.BooleanField(default=False, verbose_name='Привычка опубликована')

    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'

    def __str__(self):
        if self.owner:
            return f'{self.owner.email} - {self.action} - {self.place} - {self.date_completion}'
        return f'No owner - {self.action} - {self.place} - {self.date_completion}'
