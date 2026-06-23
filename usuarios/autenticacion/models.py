from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_deleted = models.BooleanField(default=False)

    def has_role(self, role_name):
        return self.groups.filter(name=role_name).exists()
        
    def get_roles(self):
        return list(self.groups.values_list('name', flat=True))

    def __str__(self):
        return self.username
