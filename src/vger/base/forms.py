from django.forms import ModelForm
from base.models import Survey

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
