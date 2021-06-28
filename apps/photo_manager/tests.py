import factory
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class TestPhotoViewSet(TestCase):

    def test_create(self):
        data = {'photo': Image.new('RGB', (250, 250), (255, 255, 255))}

        response = Client().post(reverse('photo_manager:photo-list'), json=data)

        self.assertEqual(response.status_code, 403)
