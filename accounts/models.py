from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
    is_store_manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group_name = 'StoreManager' if self.is_store_manager else 'Customer'
        group = Group.objects.get(name=group_name)
        self.groups.add(group)

    def __str__(self):
        return self.username
