from django import forms
from .models import SurveyInstance, Survey, Category, Question
from django.forms import ModelForm

class FillSurvey(forms.ModelForm, id):
    #instance of a survey should be created before hand?
    survey = SurveyInstance.objects.get(id=id).survey

    categories = Category.objects.filter(survey=survey)
from django.forms import ModelForm


#This will forgo cleaning data for the time being
class SurveyModelFrom(ModelForm):
    """SurveyForm Class to handle data input"""
    class Meta:
        model = Survey
        fields = ['titleOfSurvey','directions']
        labels = {'titleOfSurvey': ('Survey Title')}
        help_texts = {
            'titleOfSurvey': ('Please enter a name for the survey'),
            'directions': ('Please enter any directions to take the survey') 
        }
