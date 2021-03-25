from django import forms
from .models import SurveyInstance, Survey, Category, Question
from django.forms import ModelForm


class SurveyCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        toc = kwargs.pop('instance')
        super(SurveyCategoryForm, self).__init__(*args, **kwargs)
        category = Category.objects.filter(titleOfCategory=toc).first()
        questions = Question.objects.filter(category=category)
        #TODO: Assign weights from the question in for loop
        QUESTION_WEIGHTS = (
            (0,'weight 0'),
            (1,'weight 1'),
            (2,'weight 2'),
            (3,'weight 3'),
            (4,'weight 4'),
        )
        for i, question in enumerate(questions):
            self.fields['custom_%s' % i] = forms.ChoiceField(choices=QUESTION_WEIGHTS, label=question)
        
    def category_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)
  

   


    
    

    

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
