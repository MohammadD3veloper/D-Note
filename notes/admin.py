from django.contrib import admin
from .models import Note, BookMarked

# Register your models here.
admin.site.register(Note)
admin.site.register(BookMarked)