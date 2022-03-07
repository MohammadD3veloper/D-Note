from django.contrib.auth import get_user_model
from django import forms
from .models import Note
from .widgets import DivTextarea
from .utils import check_note



class NoteForm(forms.ModelForm):
    text = forms.CharField(widget=DivTextarea(attrs={'id': 'editor'}))

    class Meta:
        model = Note
        fields = ['title','text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NoteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NoteForm, self).save(commit=False)
        instance.author = self.user
        instance.save_cover(self.cleaned_data.get("text"))
        if commit:
            instance.save()
        return instance



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'profile_photo', 'phone', 
                            'short_about', 'about', 'resume', 'intro_url', 'username', 'email']