from django.db import models
from django.conf import settings
from .tasks import async_convert
from django.core.files import File
import uuid
import os


CODE_LANGUAGE_CHOICES = (
    (1, 'Plain Text'),
    (2, 'Programming Language Code'),
)


class BookMarked(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarked')
    note = models.OneToOneField('Note', on_delete=models.CASCADE, related_name='bookmarked')


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=50)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cover_url = models.URLField(null=True, blank=True)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=1)
    public = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save_cover(self, html_str):
        result = async_convert.delay(html_str)
        url = result.get(timeout=20)
        if not self.cover_url:
            self.cover_url = url
