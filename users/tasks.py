from datetime import datetime
from celery import shared_task
from users.services import send_notification
from habit_tracker.models import Habit


@shared_task
def send_habit_notification():
    """ Отправляет уведомление о выполнении привычке """
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute
    habits = Habit.objects.filter(date_completion__hour=hour_now, date_completion__minute=minute_now)
    for habit in habits:
        reward_or_related_habit = habit.award if habit.award else (
            habit.related_habit.name if habit.related_habit else "Никакого вознаграждения или связанной с ним привычки")
        message = f'''Дружеское напоминание.
    Ваша привычка {habit.name}:
    Действие: {habit.action},
    Место: {habit.place},
    Время: {habit.date_completion}
    Награда или приятная привычка: {reward_or_related_habit}
    Время выполнения: {habit.execution_time}
Удачи!'''
        send_notification(message, habit.owner.tg_chat_id)
        print(f'{habit.owner} - {habit.action} - {habit.place} отправить '
              f'{habit.owner} ({habit.owner.telegram_nickname})')
