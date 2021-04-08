from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Advisor, Student, Administrator

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserTypeForm(forms.Form):
    ROLES = (
        ('Administrator', 'Administrator Account'),
        ('Advisor', 'Advisor Account'),
        ('Student', 'Student Account')
    )
    role = forms.ChoiceField(widget=forms.Select, choices=ROLES,)