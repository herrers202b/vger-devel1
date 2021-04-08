from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserTypeForm
from .models import Advisor, Student, Administrator


# Create your views here.
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('canCreateUser')
def registerPage(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        ut_form = UserTypeForm(request.POST)
        if form.is_valid() and ut_form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            role = ut_form.cleaned_data.get('role')
            if role == "Advisor":
                Advisor.objects.create(user=user).save()
            elif role == "Administrator":
                Administrator.objects.create(user=user).save()
            else:
                Student.objects.create(user=user).save()
            
            
            messages.success(request, 'Account was created for ' + username)

    context = {
        'form': UserCreationForm(),
        'ut_form': UserTypeForm(),
    }
    return render(request,'register.html', context)

def profilePage(request):
    if hasattr(request.user, 'advisorAccount'):
        return advisorProfile(request)
    elif hasattr(request.user, 'studentAccount'):
        return studentProfile(request)
    else:
        return adminProfile(request)
    
def advisorProfile(request):
    return render(request, 'profile/advisor_profile.html')

def studentProfile(request):
    return render(request, 'profile/student_profile.html')

def adminProfile(request):
    return render(request, 'profile/admin_profile.html')

