from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import NoteForm, UserProfileForm
from .models import Note, BookMarked
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Q
from django.http.response import JsonResponse, Http404
from .utils import check_bookmark, check_note


# Create your views here.
class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'accounts:register'
    form_class = NoteForm
    model = Note
    template_name = 'note_create.html'
    success_url = reverse_lazy('note:manage')

    def form_valid(self, form):
        if check_note(self.request.user.username):
            return super().form_valid(form)
        else:
            return JsonResponse({'error': True})

    def get_form_kwargs(self):
        kwargs = super(NoteCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Create Note"
        data['profile_photo'] = self.request.user.profile_photo
        return data


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'accounts:register'
    form_class = NoteForm
    model = Note
    template_name = 'note_update.html'
    success_url = reverse_lazy('note:manage')

    def get_form_kwargs(self):
        kwargs = super(NoteUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Update Note"
        data['profile_photo'] = self.request.user.profile_photo
        return data

    def get_object(self, queryset=None):
        if not self.request.user.is_superuser:
            return get_object_or_404(Note, uuid=self.kwargs.get('uuid'), author=self.request.user)
        return get_object_or_404(Note, uuid=self.kwargs.get('uuid'))



class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'accounts:register'
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Note, uuid=self.kwargs.get('uuid'))


class NotesManager(LoginRequiredMixin, generic.View):
    login_url = 'accounts:register'

    def get(self, request):
        notes = Note.objects.filter(author=self.request.user)
        return render(request, 'note_manager.html', {'notes': notes, 'title': 'Manage Notes', 'profile_photo': self.request.user.profile_photo})

    def post(self, request):
        result = Note.objects.filter(author=self.request.user)
        query = request.POST.get('q')
        if query:
            if not request.user.is_superuser:
                result = Note.objects.filter(Q(title__icontains=query) | Q(text__icontains=query), author=self.request.user)
            result = Note.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
        return render(request, 'note_manager.html', {'notes': result, 'title': 'Manage Notes', 'profile_photo': self.request.user.profile_photo})



class FindUsers(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:register'
    model = Note
    template_name = 'note_users.html'
    context_object_name = 'users_note'


    def get_queryset(self):
        # query = self.kwargs.get('q', None)
        query = self.request.GET.get('q', None)
        if query:
            result = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(text__icontains=query) |
                Q(author__username=query)
            )
            if result:
                return result
        else:
            return self.model.objects.all().order_by('-pk')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Find Notes"
        data['profile_photo'] = self.request.user.profile_photo
        return data



class NoteBookMark(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:register'
    model = get_user_model()
    template_name = 'note_bookmark.html'
    context_object_name = 'note_bookmark'


    def get_queryset(self):
        result = []
        query = self.request.GET.get('q', None)
        user = self.model.objects.get(pk=self.request.user.pk)
        note = user.bookmarked.all()
        for i in note:
            if query:
                if query in i.note.title or query in i.note.text:
                    result.append(i.note)
            else:
                result.append(i.note)
        return result

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Bookmarks"
        data['profile_photo'] = self.request.user.profile_photo
        return data



class NoteDeleteView(LoginRequiredMixin, generic.View):
    login_url = 'accounts:register'

    def get(self, request):
        uuid = request.GET.get('uuid')
        try:
            note = get_object_or_404(Note, uuid=uuid, author=self.request.user)
            if note:
                note.delete()
                return JsonResponse({
                'success': True
            })
            return JsonResponse({
                'error': True
            })
        except Note.DoesNotExist:
            return JsonResponse({
                'error': 'Not Found'
            })



class UpdateProfile(LoginRequiredMixin, generic.View):
    login_url = 'accounts:register'

    def get(self, request):
        try:
            user = get_user_model().objects.get(pk=request.user.pk)
        except get_user_model().DoesNotExist:
            return Http404()
        form = UserProfileForm(instance=user)
        return render(request, 'settings.html', {'form': form, 'title': 'Update Profile',
        'profile_photo': user.profile_photo})

    def post(self, request):
        user = get_user_model().objects.get(pk=request.user.pk)
        form = UserProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('note:manage')

        return render(request, 'settings.html', {'form': form, 'title': 'Update Profile',
        'profile_photo': user.profile_photo})


def bookmark(request):
    if request.method == "GET":
        cr = request.GET.get("cr")
        uuid = request.GET.get("uuid")
        note = Note.objects.get(uuid=uuid)
        if cr == "create":
            if check_bookmark(request.user.username):
                BookMarked.objects.create(
                    user=request.user,
                    note=note
                )
                return JsonResponse({
                    'create_success': True
                })
            else:
                return JsonResponse({
                    'error': 'You cannot add bookmarks more than 10 times'
                })
        elif cr == "remove":
            bk = BookMarked.objects.get(
                user=request.user,
                note=note
            )
            bk.delete()
            return JsonResponse({
                'remove_success': True
            })



def pub_note(request):
    if request.method == "GET":
        cr = request.GET.get("cr")
        uuid = request.GET.get("uuid")
        note = Note.objects.get(uuid=uuid)
        if note.author == request.user:
            if cr == "create":
                note.public = True
                note.save()
                return JsonResponse({
                    'create_success': True
                })
            elif cr == "remove":
                note.public = False
                note.save()
                return JsonResponse({
                    'remove_success': True
                })
        else:
            return JsonResponse({
                'error': "You cannot public the note that you arent owned"
            })


def donate(request):
    return render(request, 'donate.html', {'title': "Donate US", "profile_photo": request.user.profile_photo})


class NotesStats(LoginRequiredMixin, generic.View):
    login_url = 'accounts:register'

    def get(self, request):
        user = get_user_model().objects.get(pk=request.user.pk)
        user_notes_count = user.note_set.all().count()
        user_bookmarks = user.bookmarked.all().count()
        all_bookmarks = BookMarked.objects.all().count()
        all_notes = Note.objects.all().count()
        all_users = get_user_model().objects.all().count()
        return render(
            request,
            'stats.html',
            {
                'user_notes_count': user_notes_count,
                'user_bookmarks': user_bookmarks,
                'all_notes': all_notes,
                'all_users': all_users,
                'all_bookmarks': all_bookmarks
            })



class UsersProfile(LoginRequiredMixin, generic.DetailView):
    login_url = 'accounts:register'
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))