from django.contrib import admin
from habit_tracker.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_owner_email', 'place', 'date_completion', 'action', 'is_pleasant', 'related_habit',
                    'award', 'periodicity', 'execution_time', 'is_public',)
    list_filter = ('is_pleasant', 'is_public')
    search_fields = ('name', 'owner__email', 'owner__telegram_nickname', 'place', 'action', 'award')
    ordering = ('date_completion', 'id',)

    def get_owner_email(self, obj):
        return obj.owner.email if obj.owner else "Нет данных"

    get_owner_email.short_description = 'E-mail пользователя'
