from extensions.write_on_pic import convert
from celery import shared_task


@shared_task
def async_convert(html_str):
    url = convert(html_str)
    return url
