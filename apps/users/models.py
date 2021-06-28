from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    can_upload = models.BooleanField('Can upload photo', default=True)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.username
