from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = None
    first_name = None
    last_name = None

    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255)

    status = models.CharField(
        choices=[
            ('agent', 'AGENT'),
            ('admin', 'ADMIN'),
        ]
    )
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)