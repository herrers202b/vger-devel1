from django.shortcuts import render

from .models import Survey, Category, Question
# Create your views here.
def home(request):
    return render(request, 'home.html')