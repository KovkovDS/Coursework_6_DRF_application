from datetime import time, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from habit_tracker.models import Habit


User = get_user_model()


class HabitTestCase(APITestCase):
    """Тесты для работы с привычками."""
    @classmethod
    def setUpTestData(cls):
        """ Метод класса с начальными данными для тестов."""
        cls.user = User.objects.create(email='test@test.com')
        cls.habit = Habit.objects.create(
            name='Тест привычки',
            place='Где-нибудь',
            date_completion='04:20:00',
            action='Что-нибудь',
            is_pleasant=False,
            periodicity=4,
            award='Что-нибудь',
            execution_time=timedelta(seconds=90),
            is_public=True,
            owner=cls.user,
            related_habit=None
        )

    def setUp(self):
        """Задает начальные данные для тестов."""
        self.client.force_authenticate(user=self.user)

    def create_habit(self, **kwargs):
        """Создает привычку с заданными аргументами (или по умолчанию)."""
        defaults = {
            'name': 'Тест привычки',
            'place': 'Где-нибудь',
            'date_completion': '04:20:00',
            'action': 'Что-нибудь',
            'is_pleasant': False,
            'periodicity': 4,
            'award': 'Что-нибудь',
            'execution_time': timedelta(seconds=90),
            'is_public': True,
            'owner': self.user,
            'related_habit': None
        }
        defaults.update(kwargs)
        return Habit.objects.create(**defaults)

    def test_habit_create(self):
        """Тест создания новой привычки."""
        url = reverse('habit_tracker:adding_habit')
        response = self.client.post(url, {
            'name': 'Тест привычки',
            'place': 'Где-нибудь',
            'date_completion': '04:20:00',
            'action': 'Что-нибудь',
            'is_pleasant': False,
            'periodicity': 4,
            'award': 'Что-нибудь',
            'execution_time': '00:01:30',
            'is_public': True,
            'owner': self.user.id,
            'related_habit': ''
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(Habit.objects.last().name, 'Тест привычки')
        self.assertEqual(Habit.objects.last().place, 'Где-нибудь')
        self.assertEqual(Habit.objects.last().date_completion, time(4, 20))
        self.assertEqual(Habit.objects.last().action, 'Что-нибудь')
        self.assertEqual(Habit.objects.last().is_pleasant, False)
        self.assertEqual(Habit.objects.last().periodicity, 4)
        self.assertEqual(Habit.objects.last().award, 'Что-нибудь')
        self.assertEqual(Habit.objects.last().execution_time, timedelta(seconds=90))
        self.assertEqual(Habit.objects.last().is_public, True)
        self.assertEqual(Habit.objects.last().owner, self.user)
        self.assertEqual(Habit.objects.last().related_habit, None)

    def test_habit_list(self):
        """Тест на получение списка привычек."""
        url = reverse('habit_tracker:habits')
        habit_1 = self.create_habit(name='Habit 1', place='Place 1')
        habit_2 = self.create_habit(name='Habit 2', place='Place 2')

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertIsNone(data['next'])
        self.assertIsNone(data['previous'])

        expected_results = [
            {
                'id': self.habit.id,
                'name': self.habit.name,
                'place': self.habit.place,
                'date_completion': '04:20:00',
                'action': self.habit.action,
                'is_pleasant': self.habit.is_pleasant,
                'periodicity': self.habit.periodicity,
                'award': self.habit.award,
                'execution_time': '00:01:30',
                'is_public': self.habit.is_public,
                'owner': self.user.id,
                'related_habit': self.habit.related_habit
            },
            {
                'id': habit_1.id,
                'name': 'Habit 1',
                'place': 'Place 1',
                'date_completion': '04:20:00',
                'action': 'Что-нибудь',
                'is_pleasant': False,
                'periodicity': 4,
                'award': 'Что-нибудь',
                'execution_time': '00:01:30',
                'is_public': True,
                'owner': self.user.id,
                'related_habit': None
            },
            {
                'id': habit_2.id,
                'name': 'Habit 2',
                'place': 'Place 2',
                'date_completion': '04:20:00',
                'action': 'Что-нибудь',
                'is_pleasant': False,
                'periodicity': 4,
                'award': 'Что-нибудь',
                'execution_time': '00:01:30',
                'is_public': True,
                'owner': self.user.id,
                'related_habit': None
            },
        ]
        self.assertCountEqual(data['results'], expected_results)

    def test_habit_retrieve(self):
        """Тест получения привычки по Primary Key."""
        url = reverse('habit_tracker:habit', kwargs={'pk': self.habit.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.habit.id,
            'name': self.habit.name,
            'place': self.habit.place,
            'date_completion': self.habit.date_completion,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'periodicity': self.habit.periodicity,
            'award': self.habit.award,
            'execution_time': '00:01:30',
            'is_public': self.habit.is_public,
            'owner': self.user.id,
            'related_habit': self.habit.related_habit
        }
        self.assertEqual(response.data, expected_data)

    def test_habit_update(self):
        """Тест изменения привычки по Primary Key."""
        url = reverse('habit_tracker:update_habit', kwargs={'pk': self.habit.id})
        updated_data = {
            'name': 'Updated Habit',
            'place': 'Somewhere',
            'date_completion': '05:30:00',
            'action': 'Something',
            'is_pleasant': False,
            'periodicity': 2,
            'award': 'Something',
            'execution_time': '00:02:00',
            'is_public': False,
            'owner': self.user.id,
            'related_habit': None
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, updated_data['name'])
        self.assertEqual(self.habit.place, updated_data['place'])
        self.assertEqual(self.habit.date_completion, time(hour=5, minute=30))
        self.assertEqual(self.habit.action, updated_data['action'])
        self.assertEqual(self.habit.is_pleasant, updated_data['is_pleasant'])
        self.assertEqual(self.habit.periodicity, updated_data['periodicity'])
        self.assertEqual(self.habit.award, updated_data['award'])
        self.assertEqual(self.habit.execution_time, timedelta(seconds=120))
        self.assertEqual(self.habit.is_public, updated_data['is_public'])
        self.assertEqual(self.habit.owner.id, updated_data['owner'])
        self.assertEqual(self.habit.related_habit, updated_data['related_habit'])

    def test_habit_delete(self):
        """Тест удаления привычки по Primary Key."""
        url = reverse('habit_tracker:delete_habit', kwargs={'pk': self.habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())
