from .models import Note, BookMarked


def check_note(username):
    all_objects_count = Note.objects.filter(author__username=username).count()
    print(all_objects_count)
    if all_objects_count >= 8:
        return False
    return True


def check_bookmark(username):
    all_objects_count = BookMarked.objects.filter(user__username=username).count()
    if all_objects_count >= 10:
        return False
    return True
