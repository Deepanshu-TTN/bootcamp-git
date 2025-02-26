from django.test import TestCase
from .models import AppModel


class MyAppTestCase(TestCase):
    def setUp(self):
        self.test_model = AppModel.objects.create(some_field='some value')

    def test_object_exists(self):
        self.assertEqual(self.test_model.some_field,'some value')

# Create your tests here.
