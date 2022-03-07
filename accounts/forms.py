from django.core.validators import ValidationError
from django.core.cache import cache
from django import forms
from django.contrib.auth import get_user_model



class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput())
    code = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        code = self.cleaned_data.get('code')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        main_code = cache.get(email)
        if main_code:
            if int(main_code) == int(code):
                if not get_user_model().objects.filter(email=email).count() > 0:
                    if self.request.META.get("HTTP_X_FORWARDED_FOR"):
                        ip_addr = self.request.META.get("HTTP_X_FORWARDED_FOR")
                    else:
                        ip_addr = self.request.META.get("HTTP_REMOTE_ADDR")
                    user = get_user_model().objects.create(
                        email=email,
                        username=username,
                        ip_addr=ip_addr,
                        user_agent=self.request.META.get("HTTP_USER_AGENT")
                    )
                    if password == password_confirm:
                        user.set_password(password_confirm)
                        user.is_active = True
                        user.save()
                        cache.delete(email)
                    else:
                        self.add_error("password_confirm", "Passwords do not match")
                else:
                    self.add_error("email", "This email address is already exist.")
            else:
                self.add_error("code", "code is invalid")
        else:
            self.add_error("code", "code is expired")


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
