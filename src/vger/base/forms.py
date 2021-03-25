from django import forms
from .models import SurveyInstance, Survey, Category, Question
from django.forms import ModelForm


class SurveyCategoryForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.titleOfCategory = kwargs.pop('titleOfCategory')
        super(SurveyCategoryForm,self).__init__(*args,**kwargs)
        
        self.fields['titleOfCategory'] = forms.CharField(widget=forms.te)
        self.fields['titleOfCategory'].widget = forms.TextInput(attrs={'titleOfCategory':titleOfCategory})
    
    print(forms.CharField())
    # category = Category.objects.get(titleOfCategory=forms.CharField())
    # print(category)
    
    

    

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
