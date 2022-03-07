from django.shortcuts import render, redirect
from django.views import generic
from .forms import UserLoginForm, UserRegistrationForm
from django.http.response import JsonResponse
from .tasks import sendemail
from django.core.cache import cache
from .utils import random_code
from django.contrib.auth import authenticate, login, logout, get_user_model



# Create your views here.
class Register(generic.View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request=request)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('note:manage')
        return render(request, 'register.html', {'form': form})



class Login(generic.View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'success': True
            })
        return JsonResponse({
            'error': 'user does not exist'
        })


def logout(request):
    try:
        logout(request)
        user = get_user_model().objects.get(pk=request.user.pk)
        user.delete()
    except get_user_model().DoesNotExist:
        logout(request)



def send_code(request):
    email = request.GET.get("email")
    code = random_code()
    cache.set(email, code, 2600)
    subject = "Verify EmailAddress"
    html_text = f"""
    <h2>Hello dear {email}</h2>
    <p>Welcome to our website</p>
    <p>here is your code: <b>{code}</b></p>
    <b>Thanks for choosing us</b>
    """
    sendemail.delay(subject, html_text, email)
    return JsonResponse({
        'success': True,
    })
