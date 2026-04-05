from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # We can add fields if necessary. 
    # For now, we will rely on Django's built-in groups and permissions 
    # to handle 'Roles' like in Spatie, mapped to Django's Group model.
    # We will provide helper properties for role checking if needed.

    def has_role(self, role_name):
        return self.groups.filter(name=role_name).exists()
        
    def get_roles(self):
        return list(self.groups.values_list('name', flat=True))

    def __str__(self):
        return self.username
