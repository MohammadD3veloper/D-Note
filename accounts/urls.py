from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('send-code/', views.send_code, name='scode'),
    path('logout/', views.logout, name="logout")
    # path('profile/detail/', views.UpdateProfile.as_view(), name='profile_detail'),
]