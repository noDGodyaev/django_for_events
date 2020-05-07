from django.forms import ModelForm, Form
from . import models
from django import forms
from django.http import HttpResponse
from django.core.validators import URLValidator, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Org
from .models import Participant


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class PartForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [field.name for field in Participant._meta.fields]
