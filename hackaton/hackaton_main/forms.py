from django.forms import ModelForm
from .models import UserTask
from django_ace import AceWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CodeForm(forms.Form):
    text = forms.CharField(widget=AceWidget(mode='c_cpp', theme='twilight'))

from django import forms


class EditorForm(forms.Form):
    """エディタ部分となるフォーム."""
    code = forms.CharField(
        widget=forms.Textarea,
    )