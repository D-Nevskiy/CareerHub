from django.test import TestCase
from rest_framework.test import APIClient

class StudentViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создайте здесь необходимые студенты для тестирования

    def test_student_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 404)