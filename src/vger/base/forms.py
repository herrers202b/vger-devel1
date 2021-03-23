from .models import Survey, Category, Question
from django.forms import ModelForm

class SurveyForm(ModelForm):
    class Mtea:
        model = Survey
        fields = ['titleOfSurvey', 'directions', 'created', 'lastUpdated']