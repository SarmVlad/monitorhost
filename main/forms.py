from django import forms
from monitorhost import settings
import os

class UploadImgForm(forms.Form):
    file = forms.ImageField()

def handle_uploaded_user_img(f):
    with open (os.path.normpath("%s%s%s%s%s" %(os.getcwd(),"/main", settings.MEDIA_URL, "profile_photo/", f.name)), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)