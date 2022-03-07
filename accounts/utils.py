from django.core.exceptions import ValidationError
from os.path import splitext
import random



def upload_resume_path(file):
    valid_extensions = ['.pdf']
    extension = splitext(file.name)[1]
    if not extension.lower() in valid_extensions:
        return ValidationError(f'This filetype cannot be accepted, try \
                                            {", ".join(valid_extensions)} only')

def upload_photo_path(instance, filename):
    return f"user/{instance}/photo/{filename}"


def random_code():
    return random.randrange(10000, 99999)