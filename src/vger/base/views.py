from django.shortcuts import render
from .models import Survey, Category, Question, SurveyInstance
from django.views import generic

# Create your views here.
class SurveyListView(generic.ListView):
    model = Survey
    context_object_name = 'survey_list'
    #We can create our own template name as needed
    template_name = 'survey_list.html' 
