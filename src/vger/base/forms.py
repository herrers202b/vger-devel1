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
  
from django import forms
from base.models import Survey, Category, Question
#This will forgo cleaning data for the time being
class SurveyModelFrom(ModelForm):
    """
    SurveyForm Class to handle data input
    """
    class Meta:
        """
        Survey : model
            the model we will pull from to create this ModelForm
        ['titleOfSurvey','directions'] : fields
            these are the fields we are specifying in our form
        {'titleOfSurvey': ('Survey Title')} : labels
            we're specifying which label to use in place of the field text
            ex) {someLabel : (newTextHere)}
        """
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
        """
        Category : model
            the model we will pull from to create this ModelForm
        ['titleOfCategory','lowWeightText', 'highWeightText', 'survey'] : fields
            these are the fields we are specifying in our form
        {'titleOfCategory': ('Category Title')} : labels
            we're specifying which label to use in place of the field text
            ex) {someLabel : (newTextHere)}
        """
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
        """
        Question : model
            the model we will pull from to create this ModelForm
        ['questionText','answer', 'questionNumber'] : fields
            these are the fields we are specifying in our form
        """
        model = Question
        fields = ['questionText','answer', 'questionNumber']
    #category = forms.ModelChoiceField(queryset=Category.objects.filter(id=1))