from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, unique=True)
    date_joined = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    job_title = models.CharField(max_length=100, default='Unemployed')
    website = models.URLField(null=True, blank=True)
    github = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.email

    def get_fullname(self):
        return self.first_name + ' ' + self.last_name


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveBigIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.phone_number} - {self.code} - {self.created}'
