import requests

HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
# Retrieve these from https://htmlcsstoimage.com/dashboard
HCTI_API_USER_ID = '06632542-7a5f-45f0-bf6b-276e8ffe86df'
HCTI_API_KEY = '60cbe624-c542-49af-b0b3-288fd12e850c'


def convert(html_str):
    data = { 'html': html_str,
             'google_fonts': "Nunito" }
    image = requests.post(url = HCTI_API_ENDPOINT, data = data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    return image.json()['url']
