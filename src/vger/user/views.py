from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Advisor, Student, Administrator


# Create your views here.
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('canCreateUser')
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('home-page')

    context = {'form': form}
    return render(request,'register.html', context)
