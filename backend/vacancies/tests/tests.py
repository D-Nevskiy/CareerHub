from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from students.models import Student
from shared_info.models import Location, Specialization, Course, EducationLevel, Schedule, Skill
from vacancies.models import Vacancy


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

        self.schedule = Schedule.objects.create(name='Гибкий график')
        self.skill = Skill.objects.create(name='Python')
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
            education_level=self.education_level,
        )
        self.student.schedule.set([self.schedule])
        self.student.skills.set([self.skill])

        self.vacancy = Vacancy.objects.create(
            name='Python-разработчик',
            author=self.user,
            location=self.location,
            text='Берем всех',
            salary='50$'
        )
        self.vacancy.schedule.set([self.schedule])
        self.vacancy.required_skills.set([self.skill])
        self.vacancy.required_education_level.set([self.education_level])
        self.vacancy.specialization.set([self.specialization])

        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_vacancy_match(self):
        response = self.authorized_client.get('/api/matching/1/')
        self.assertEqual(response.status_code, 200)
        desired_vacancy_id = 2
        self.assertTrue(any(item['id'] == desired_vacancy_id for item in response.data))
