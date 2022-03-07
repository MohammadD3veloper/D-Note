from django.forms import Textarea


class DivTextarea(Textarea):
    template_name = 'django/forms/widgets/div.html'
