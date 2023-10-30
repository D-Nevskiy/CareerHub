from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from students.models import Student
from shared_info.models import Location, Specialization, Course, EducationLevel


class StudentViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@yandex.ru',
            password='123456',
            first_name='Danya',
            last_name='Nevskiy',
        )
        self.user.is_active = True

        self.location = Location.objects.create(name='Москва')
        self.specialization = Specialization.objects.create(name='Разработка')
        self.course = Course.objects.create(name='Python-разработчик')
        self.education_level = EducationLevel.objects.create(name='Junior')
        self.student = Student.objects.create(
            first_name='Иван',
            last_name='Иванов',
            location=self.location,
            specialization=self.specialization,
            course=self.course,
            age=23,
            education_level=self.education_level
        )

        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_student_favorite(self):
        """Проверка на добавление и удаление пользователя из избранных"""
        response1 = self.authorized_client.post('/api/favorite/1/')
        self.assertEqual(response1.status_code, 201)

        response2 = self.authorized_client.get('/api/favorite/')
        self.assertEqual(response2.status_code, 200)
        favorite_students = response2.data
        self.assertTrue(
            any(student['id'] == self.student.id
                for student in favorite_students)
        )

        response3 = self.authorized_client.delete(
            f'/api/favorite/{self.student.id}/'
        )
        self.assertEqual(response3.status_code, 204)

        response4 = self.authorized_client.get('/api/favorite/')
        self.assertEqual(response4.status_code, 200)
        favorite_students_after_deletion = response4.data
        self.assertFalse(
            any(student['id'] == self.student.id
                for student in favorite_students_after_deletion)
        )
