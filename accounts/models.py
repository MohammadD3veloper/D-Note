from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .utils import upload_photo_path, upload_resume_path
from django.urls import reverse_lazy



# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    ip_addr = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=250, null=True)
    profile_photo = models.ImageField(upload_to=upload_photo_path, blank=True, null=True)
    phone_regex = RegexValidator(regex='^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$', message='You should enter the correct phone numgber.')
    phone = models.CharField(max_length=11, validators=[phone_regex], blank=True, null=True)
    short_about = models.CharField(max_length=170)
    about = models.TextField(max_length=400, blank=True, null=True)
    resume = models.FileField(upload_to=upload_resume_path, blank=True, null=True)
    intro_url = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return first_name + last_name

    def get_absolute_url(self):
        return reverse_lazy("note:user-profile", kwargs={"username": self.username})