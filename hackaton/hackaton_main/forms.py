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

class EditorForm(forms.Form):
    PROGRAMMING_LANGUAGES = (
        ('1', 'python'),
        ('2', 'ruby')
    )
    language = forms.ChoiceField(choices=PROGRAMMING_LANGUAGES, widget=forms.Select(attrs={"onchange":"changeLanguage()"}))
    code = forms.CharField(widget=forms.Textarea)
