from django.contrib.auth import get_user_model
from django.db import models

from django_softdelete.models import SoftDeleteModel

User = get_user_model()


def get_upload_path(instance, filename):
    """Возвращает путь для загрузки фотографий пользователя"""
    return '/'.join(['photos', str(instance.user.pk), filename])


class Photo(SoftDeleteModel):
    user = models.ForeignKey(User, related_name='user_photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_upload_path)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.photo.name
