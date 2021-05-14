from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.fields import DateField
from .widgets import XDSoftDateTimePickerInput
from .models import Survey, Category, Question, Survey_Question, Option_Choice, Input_Type, Option_Group
from django.forms import HiddenInput, Select
from django.forms.models import ModelChoiceField, ModelChoiceIterator


class NewVersionForm(forms.Form):
    
    version_number = forms.DecimalField(max_digits=5, decimal_places=2)

class SurveyCreateForm(forms.ModelForm):
    """
    SurveyCreateForm

    This form is for creating a survey and is currently unfinished

    """
    class Meta:
        model = Survey
        fields = ('titleOfSurvey', 'version_number', 'description', 'start_date', 'end_date')
        widgets = {
            'start_date': XDSoftDateTimePickerInput(),
            'end_date': XDSoftDateTimePickerInput(),
        }

        
class CategoryCreateForm(forms.Form):
    """
    CategoryCreateForm

    Class form used to create a category from a view

    title_of_category : CharField
        the title of a category with a 100 char max lenght

    More : BooleanField

    type : ChoiceField

    """
    title_of_category = forms.CharField(max_length=100)
    More = forms.BooleanField(required=False, widget=HiddenInput())
    type = forms.ChoiceField(choices = ((1, 'One'), (2, 'Two')))

    # Use any form fields you need, CharField for simplicity reasons
    list1 = forms.CharField()
    list2 = forms.CharField()

class QuestionChoiceField(ModelChoiceField):
    """
    QuestionChoiceField

    Custom ModelChoiceField used to take an input type for questions
    and mask the raw object name with its actual type name for usability
    """
    def label_from_instance(self, obj):
            return f'{obj.input_type_name}'

class OptionChoiceField(ModelChoiceField):
    """
    OptionChoiceField

    Custom ModelChoiceField used to take a quesiton group object for
    questions and mask the raw object name with its actual group name
    for usability
    """
    def label_from_instance(self, obj):
            return f'{obj.name_of_group}'

class QuestionCreateForm(forms.ModelForm):
    """
    QuiestionCreateForm

    ModelForm that handles creating a question from scratch.

    input_type_fk : QuestionChoiceField
        form field that takes the input_type foreign key and
        then uses a method to mask the object name with its
        type name field.

    option_group : OptionChoiceField
        same as input_type directly above but for question
        option groups.
    """
    input_type_fk = QuestionChoiceField(queryset=Input_Type.objects,
                                            widget=Select(),
                                            label="Question type")
    option_group = OptionChoiceField(queryset=Option_Group.objects,
                                            widget=Select(), required=False)

    class Meta:
        model = Question
        fields = ('question_text',
            'answer_is_required',
            'is_multi_option_answer',
            'input_type_fk',
            'option_group')
        labels = {
            'answer_is_required': 'Is an answer required for this question?',
            'is_multi_option_answer': 'Is this a multiple choice question?',
        }


class OptionGroupForm(forms.ModelForm):
    class Meta:
        model = Option_Group
        fields = ('name_of_group',)
        labels = {'name_of_group':'Name of this option group:'}

class OptionChoiceForm(forms.ModelForm):
    class Meta:
        model = Option_Choice
        fields = ('choice_text',)
        labels = {'choice_text': 'Enter some text for this particular choice.'}


class OptionGroupChoiceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(OptionGroupChoiceForm, self).__init__(*args, **kwargs)
        self.fields['name_of_group'] = forms.CharField(
            label='Name of this option group:'
        )

        for i in range(5):
            name = 'custom_%s' % i
            self.fields[name] = forms.CharField(
                label=i
            )

    def option_choice(self):
        for name, value in self.cleaned_data.items():
            print(name.split('_'), value)
            if name.startswith('custom_'):
                yield (name.split('_')[1], value)
#TODO: Refactor form to approprately gather question answer groups
class SurveyCategoryForm(forms.Form):
    """
    SurveyCategoryForm

    This form is used for creating a number of questions based on
    how many are in a category dynamically and the returning those
    in a form

    @kwargs = Primary key of the category table entry
    """
    def __init__(self, *args, **kwargs):
        toc = kwargs.pop('instance')
        super(SurveyCategoryForm, self).__init__(*args, **kwargs)
        category = Category.objects.get(pk=toc)
        survey_questions = Survey_Question.objects.filter(category_fk=category)

        for i, survey_question in enumerate(survey_questions):
            question = survey_question.question_fk


            option_choices = Option_Choice.objects.filter(option_group=question.option_group)

            options = ((o_c.choice_text, o_c.choice_text) for o_c in option_choices)
            #This is for multi field questions
            name = 'custom_%s' % i
            print(question.input_type_fk.input_type_name)
            if question.input_type_fk.input_type_name == 'range':
                self.fields[name + ' ' + str(survey_question.pk)] = forms.ChoiceField(
                    widget=forms.RadioSelect,
                    choices=options,
                    label=question.question_text
                )
            elif question.input_type_fk.input_type_name == 'text':
                self.fields[name + ' ' + str(survey_question.pk)] = forms.CharField(
                    label=question.question_text
                )

            else:
                self.fields[name + ' ' + str(survey_question.pk)] = forms.ChoiceField(
                    widget=forms.RadioSelect,
                    choices=(
                        ('t', "True"),
                        ('f', "False")
                    ),
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
