from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class VacancyViewSetTest(APITestCase):
    def setUp(self):
        self.email = 'anarant91@gmail.com'
        self.first_name = 'Danya'
        self.last_name = 'Nevskiy'
        self.telegram = 't.me/dnevskiy'
        self.phone_number = '899999999'
        self.company = 'Ozon'

    def test_user_creation_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', first_name=self.first_name, last_name=self.last_name)

    def test_create_users(self):
        user = User.objects.create_user(email='anarant91@gmail.com', first_name='Danya', last_name='Nevskiy',
                                        password='123456', telegram='t.me/dnevskiy', phone_number='899999999',
                                        company='Ozon')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.telegram, self.telegram)
        self.assertEqual(user.phone_number, self.phone_number)
        self.assertEqual(user.company, self.company)
