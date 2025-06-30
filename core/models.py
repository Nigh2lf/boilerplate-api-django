from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone


def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError(_('Users must have an email'))

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser): 
    TYPE_USER = (
        ('ADMIN', 'ADMIN'),
        ('USER', 'USER'),
    )

    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    forgot_password_hash = models.CharField(max_length=255, null=True, blank=True)
    forgot_password_expire = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin