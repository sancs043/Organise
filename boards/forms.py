# dwitter/forms.py

from django import forms
from .models import Activity

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        exclude = ("user", )

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(max_length=150)
    surname = forms.CharField(max_length=150)

    class Meta:
        exclude = ("user", )

class CreateActivity(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.SelectDateWidget())
    maxPeople = forms.IntegerField()
    location = forms.CharField(max_length=50)


class EditActivity(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.SelectDateWidget())
    maxPeople = forms.IntegerField()
    location = forms.CharField(max_length=50)

