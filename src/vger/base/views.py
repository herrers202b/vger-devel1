from django.shortcuts import render

from .models import Survey, Category, Question, SurveyInstance
# Create your views here.
def home(request):
    return render(request, 'home.html')