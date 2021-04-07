from django import forms
# from .models import SurveyInstance, Survey, Category, Question
# from django.forms import ModelForm
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.fields import DateField
from .widgets import XDSoftDateTimePickerInput
from .models import Survey, Category, Question, Survey_Question, Option_Choice
from django.forms import HiddenInput

class SurveyCreateForm(forms.ModelForm):
    
    class Meta:
        model = Survey
        fields = ('titleOfSurvey', 'description', 'start_date', 'end_date')
        widgets = {
            'start_date': XDSoftDateTimePickerInput(),
            'end_date': XDSoftDateTimePickerInput(),
        }

class CategoryCreateForm(forms.Form):
    title_of_category = forms.CharField(max_length=100)
    More = forms.BooleanField(required=False, widget=HiddenInput())
    type = forms.ChoiceField(choices = ((1, 'One'), (2, 'Two')))

    # Use any form fields you need, CharField for simplicity reasons
    list1 = forms.CharField()
    list2 = forms.CharField()



#TODO: Refactor form to approprately gather question answer groups
class SurveyCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        toc = kwargs.pop('instance')
        super(SurveyCategoryForm, self).__init__(*args, **kwargs)
        category = Category.objects.get(pk=toc)
        survey_questions = Survey_Question.objects.filter(category_fk=category)
        
        for i, survey_question in enumerate(survey_questions):
            question = survey_question.question_fk
            #TODO: Design logic here for answer formatting in field types

            option_choices = Option_Choice.objects.filter(option_group=question.option_group)

            options = ((o_c.choice_text, o_c.choice_text) for o_c in option_choices)
            forms.ChoiceField
            #This is for multi field questions
            name = 'custom_%s' % i
            self.fields[name + ' ' + str(survey_question.pk)] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=options,
                label=question.question_text
            )
            
        
    def category_answers(self):   
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (name.split()[1], value)
  

   


    
    

    

# #This will forgo cleaning data for the time being
# class SurveyModelFrom(ModelForm):
#     """
#     SurveyForm Class to handle data input
#     """
#     class Meta:
#         """
#         Survey : model
#             the model we will pull from to create this ModelForm
#         ['titleOfSurvey','directions'] : fields
#             these are the fields we are specifying in our form
#         {'titleOfSurvey': ('Survey Title')} : labels
#             we're specifying which label to use in place of the field text
#             ex) {someLabel : (newTextHere)}
#         """
#         model = Survey
#         fields = ['titleOfSurvey','directions']
#         labels = {'titleOfSurvey': ('Survey Title')}
#         help_texts = {
#             'titleOfSurvey': ('Please enter a name for the survey'),
#             'directions': ('Please enter any directions to take the survey') 
#         }

# class CategoryModelForm(ModelForm):
#     """
#     CategoryForm to handle data input
#     """
#     class Meta:
#         """
#         Category : model
#             the model we will pull from to create this ModelForm
#         ['titleOfCategory','lowWeightText', 'highWeightText', 'survey'] : fields
#             these are the fields we are specifying in our form
#         {'titleOfCategory': ('Category Title')} : labels
#             we're specifying which label to use in place of the field text
#             ex) {someLabel : (newTextHere)}
#         """
#         model = Category
#         fields = ['titleOfCategory','lowWeightText', 'highWeightText', 'survey']
#         labels = {'titleOfCategory': ('Category Title')}
#         help_texts = {'titleOfCategory': ('Please enter a name for the category')}
#     #survey = forms.ModelChoiceField(queryset=Survey.objects.filter(id=0))
    

# class QuestionModelForm(ModelForm):
#     """
#     QuestionModelFrom to handle data input
#     """
#     class Meta:
#         """
#         Question : model
#             the model we will pull from to create this ModelForm
#         ['questionText','answer', 'questionNumber'] : fields
#             these are the fields we are specifying in our form
#         """
#         model = Question
#         fields = ['questionText','answer', 'questionNumber']
#     #category = forms.ModelChoiceField(queryset=Category.objects.filter(id=1))