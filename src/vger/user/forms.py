from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import customUser
from django.contrib.auth.models import User
from .models import Advisor, Student, Administrator

class CreateUserForm(UserCreationForm):
    class Meta:
        model = customUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
