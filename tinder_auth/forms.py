from tinder_app.models import *
from django.contrib.auth.models import User
from django import forms

class RegisterInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['main_photo', 'description', 'sub_type']
