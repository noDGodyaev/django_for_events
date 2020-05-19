from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Participant


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class PartForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [field.name for field in Participant._meta.fields]
