from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            user_1 = User.objects.create_user('Ivanov', password='1234567890', email='ivanov12543@gmail.com')
            user_2 = User.objects.create_user('Petrov', password='0987654321', email='petriv1989.43@gmail.com',
                                              is_staff=True)
            user_3 = User.objects.create_superuser('Sidorov', password='567890', email='sidorov12543@gmail.com')
        except Exception as e:
            print("Пользователь уже существует")
            print(e)
