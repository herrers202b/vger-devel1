from django import forms
from .models import SurveyInstance, Survey, Category, Question

class FillSurvey(forms.ModelForm, id):
    #instance of a survey should be created before hand?
    survey = SurveyInstance.objects.get(id=id).survey

    categories = Category.objects.filter(survey=survey)