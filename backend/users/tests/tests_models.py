from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            email='testemail.yandex.ru',
            first_name='Danya',
            last_name='Nevskiy',
            password='123456'
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        user = UserModelTest.user
        field_verboses = {
            'avatar': 'Изображение профиля',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'telegram': 'Ссылка на Telegram',
            'phone_number': 'Номер телефона',
            'company': 'Компания',
            'role': 'Роль'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        user = UserModelTest.user
        field_help_texts = {
            'phone_number': 'Введите номер телефона',
            'telegram': 'Введите ссылку на Telegram',
            'company': 'Введите название вашей компании',
            'avatar': 'Загрузите картинку',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).help_text, expected_value)

    def test_invalid_phone_number(self):
        """Проверка валидации номера телефона."""
        user = UserModelTest.user
        invalid_phone_numbers = ['12345', '12345678901234567890', 'abc12345']
        for phone_number in invalid_phone_numbers:
            with self.subTest(phone_number=phone_number):
                user.phone_number = phone_number
                with self.assertRaises(ValidationError):
                    user.full_clean()
