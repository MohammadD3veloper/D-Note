from django.urls import path
from . import views


app_name = 'note'

urlpatterns = [
    path('', views.NoteCreateView.as_view(), name='create'),
    path('manage/', views.NotesManager.as_view(), name='manage'),
    path('update/<uuid>/', views.NoteUpdateView.as_view(), name='update'),
    path('detail/<uuid>/', views.NoteDetailView.as_view(), name='detail'),
    path('delete/', views.NoteDeleteView.as_view(), name='delete'),
    path('settings/', views.UpdateProfile.as_view(), name='settings'),
    path('find/', views.FindUsers.as_view(), name='find'),
    path('profile/<str:username>/', views.UsersProfile.as_view(), name="user-profile"),
    path('note/pub/', views.pub_note, name='pub-note'),
    path('bookmark/', views.NoteBookMark.as_view(), name='bookmark'),
    path('bookmark/add/', views.bookmark, name='add-bookmark'),
    path('stats/', views.NotesStats.as_view(), name='stats'),
    path('donate/', views.donate, name="donate"),
]