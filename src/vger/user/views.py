from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserTypeForm
from .models import Advisor, Student, Administrator
from base.models import User_Survey


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
    surveys = User_Survey.objects.filter(user_fk = request.user)

    if hasattr(request.user, 'advisorAccount'):
        return advisorProfile(request, surveys)
    elif hasattr(request.user, 'studentAccount'):
        return studentProfile(request, surveys)
    else:
        return adminProfile(request, surveys)

def advisorProfile(request, surveys):
    advisor = Advisor.objects.get(user = request.user)
    advised_student_list = Student.objects.filter(advisor = advisor)
    context = {
        'surveys': surveys,
        'advised_student_list': advised_student_list,
    }
    return render(request, 'profile/advisor_profile.html', context = context)

def studentProfile(request, surveys):
    return render(request, 'profile/student_profile.html', {'surveys' : surveys})

def adminProfile(request, surveys):
    return render(request, 'profile/admin_profile.html', {'surveys' : surveys})
