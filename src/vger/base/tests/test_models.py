from django.contrib.auth.models import User
from django.test import TestCase

#=======================================================================

#Try to import the Question model from models.py
try:
    from ..models import Question
except ImportError:
    raise ImportError("The Question model is not implemented for testing import!")

#Try to import the Category model from models.py
try:
    from ..models import Category
except ImportError:
    raise ImportError("The Category model is not implemented for testing import!")

#Try to import the Survey model from models.py
try:
    from ..models import Survey
except ImportError:
    raise ImportError("The Survey model is not implemented for testing import!")

#Try to import the SurveyInstance model from models.py
try:
    from ..models import SurveyInstance
except ImportError:
    raise ImportError("The SurveyInstance model is not implemented for testing import!")

#|Question Test
#   1. Tests to make sure each parameter doesn't exceed the max length
#   2. Tests to check the help text
#   3. Tests to check the defult text
# |#

class QuestionTest(TestCase):
    def setUp(self):
        Question.objects.create(questionText = 'I know how to install software on my computer')

    #questionText testing
    def test_questionText_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('questionText').max_length
        self.assertEqual(max_length, 100)

    def test_questionText_helptext(self):
        question = Question.objects.get(id=1)
        help_text = question._meta.get_field('questionText').help_text
        self.assertEqual(help_text, 'Please enter a prompt. ex) I know how to install software on my computer.')

    #score testing
    def test_score_choices(self):
        question = Question.objects.get(id=1)
        choices = question._meta.get_field('answer').choices
        self.assertEqual(choices, question.QUESTION_WEIGHTS)

    def test_score_blank(self):
        question = Question.objects.get(id=1)
        blank = question._meta.get_field('answer').blank
        self.assertEqual(blank, True) 

    def test_score_null(self):
        question = Question.objects.get(id=1)
        null = question._meta.get_field('answer').null
        self.assertEqual(null, True)     

    def test_score_helptext(self):
        question = Question.objects.get(id=1)
        help_text = question._meta.get_field('answer').help_text
        self.assertEqual(help_text, 'Results of question')

    #category testing
    def test_category_name(self):
        question = Question.objects.get(id=1)
        verbose_name = question._meta.get_field('category').verbose_name
        self.assertEqual(verbose_name, 'Parent Category')    

    #def test_category_name(self):
    #    question = Question.objects.get(id=1)
    #    related_name = question._meta.get_field('category').related_name
    #    self.assertEqual(related_name, 'questions') 

    def test_survey_default(self):
        question = Question.objects.get(id=1)
        default = question._meta.get_field('category').default
        self.assertEqual(default, None)

    def test_survey_null(self):
        question = Question.objects.get(id=1)
        null = question._meta.get_field('category').null
        self.assertEqual(null, True)

    #def test_survey_on_delete(self):
    #    question = Question.objects.get(id=1)
    #    on_delete = question._meta.get_field('category').on_delete
    #    self.assertEqual(on_delete, Category.models.CASCADE) 

#|Catagory Test
#   1. Tests to make sure each parameter doesn't exceed the max length
#   2. Tests to check the help text
#   3. Tests to check the defult text
# |#
class CategoryTest(TestCase):
    def setUp(self):
        Category.objects.create(titleOfCategory = 'Computer Skills')

    #titleOfCatagory testing
    def test_titleOfCategory_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('titleOfCategory').max_length
        self.assertEqual(max_length, 100)

    def test_titleOfCategory_helptext(self):
        category = Category.objects.get(id=1)
        help_text = category._meta.get_field('titleOfCategory').help_text
        self.assertEqual(help_text, 'Please enter a title for this category, ex) Computer Skills.')

    #lowWeight testing
    def test_lowWeightText_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('lowWeightText').max_length
        self.assertEqual(max_length, 50)

    def test_lowWeightText_default(self):
        category = Category.objects.get(id=1)
        default = category._meta.get_field('lowWeightText').default
        self.assertEqual(default, 'Not like me at all')

    def test_lowWeightText_helptext(self):
        category = Category.objects.get(id=1)
        help_text = category._meta.get_field('lowWeightText').help_text
        self.assertEqual(help_text, 'Please enter flavor text for the low weight of the category, ex) Not like me at all')

    #highWeight testing
    def test_highWeightText_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('highWeightText').max_length
        self.assertEqual(max_length, 50)

    def test_highWeightText_default(self):
        category = Category.objects.get(id=1)
        default = category._meta.get_field('highWeightText').default
        self.assertEqual(default, 'Extremely like me')

    def test_highWeightText_helptext(self):
        category = Category.objects.get(id=1)
        help_text = category._meta.get_field('highWeightText').help_text
        self.assertEqual(help_text, 'Please enter flavor text for the high weight of the category, ex) Extremely like me')

    #survey testing
    def test_survey_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('survey').verbose_name
        self.assertEqual(field_label, 'Parent Survey')

    #def test_survey_related_name(self):
    #    category = Category.objects.get(id=1)
    #    related_name = category._meta.get_field('survey').related_name
    #    self.assertEqual(related_name, 'catagories')

    def test_survey_default(self):
        category = Category.objects.get(id=1)
        default = category._meta.get_field('survey').default
        self.assertEqual(default, None)

    def test_survey_null(self):
        category = Category.objects.get(id=1)
        null = category._meta.get_field('survey').null
        self.assertEqual(null, True)

    #def test_survey_on_delete(self):
    #    category = Category.objects.get(id=1)
    #    on_delete = category._meta.get_field('survey').on_delete
    #    self.assertEqual(on_delete, Category.models.CASCADE)

#|Survey Test
#   1. Tests to make sure each parameter doesn't exceed the max length
#   2. Tests to check the help text
#   3. Tests to check the defult text
# |#

class SurveyTest(TestCase):
    def setUp(self):
        Survey.objects.create(titleOfSurvey = 'Online Survey')

    #titleOfSurvey testing
    def test_titleOfSurvey_length(self):
        survey = Survey.objects.get(id=1)
        max_length = survey._meta.get_field('titleOfSurvey').max_length
        self.assertEqual(max_length, 50)

    def test_titleOfSurvey_helptext(self):
        survey = Survey.objects.get(id=1)
        help_text = survey._meta.get_field('titleOfSurvey').help_text
        self.assertEqual(help_text, 'Please enter a name for the survey')

        #directions testing
    def test_directions_length(self):
        survey = Survey.objects.get(id=1)
        max_length = survey._meta.get_field('directions').max_length
        self.assertEqual(max_length, 500)

    def test_directions_helptext(self):
        survey = Survey.objects.get(id=1)
        help_text = survey._meta.get_field('directions').help_text
        self.assertEqual(help_text, 'Please enter any directions to take the survey')