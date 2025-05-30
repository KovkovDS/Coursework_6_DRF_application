# Generated by Django 5.2 on 2025-05-11 17:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_telegram_nickname_alter_user_tg_chat_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telegram_nickname",
            field=models.CharField(
                blank=True,
                max_length=32,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_telegram_nickname",
                        message="Никнейм в Telegram должен начинаться с @ и содержать только буквы, цифры и символы подчеркивания.                     Длина: 5-32 символа.",
                        regex="^@[A-Za-z0-9_]{4,31}$",
                    )
                ],
                verbose_name="Имя пользователя в Telegram",
            ),
        ),
    ]
