from django import forms
from .models import SurveyInstance, Survey, Category, Question
from django.forms import ModelForm
from django import forms
from base.models import Survey, Category, Question
#This will forgo cleaning data for the time being
class SurveyModelFrom(ModelForm):
    """
    SurveyForm Class to handle data input
    """
    class Meta:
        model = Survey
        fields = ['titleOfSurvey','directions']
        labels = {'titleOfSurvey': ('Survey Title')}
        help_texts = {
            'titleOfSurvey': ('Please enter a name for the survey'),
            'directions': ('Please enter any directions to take the survey') 
        }

class CategoryModelForm(ModelForm):
    """
    CategoryForm to handle data input
    """
    class Meta:
        model = Category
        fields = ['titleOfCategory','lowWeightText', 'highWeightText', 'survey']
        labels = {'titleOfCategory': ('Category Title')}
        help_texts = {'titleOfCategory': ('Please enter a name for the category')}
    #survey = forms.ModelChoiceField(queryset=Survey.objects.filter(id=0))
    

class QuestionModelForm(ModelForm):
    """
    QuestionModelFrom to handle data input
    """
    class Meta:
        model = Question
        fields = ['questionText','answer', 'questionNumber']
    #category = forms.ModelChoiceField(queryset=Category.objects.filter(id=1))