import sys 
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, SimpleTestCase
from django.urls import reverse, resolve
#=======================================================================
#Try to import the survey_page view from views.py
try:
    from ..views import survey_page
except ImportError:
    raise ImportError("The survey_page view is not implemented for testing import!")
    


#Try to import the survey_question model from models.py
try:
    from ..models import survey_question
except ImportError:
    raise ImportError("The survey_page view is not implemented for testing import!")



#Try to import the survey model from models.py
try:
    from ..models import survey
except ImportError:
    raise ImportError("The survey_page view is not implemented for testing import!")

#=======================================================================

class SurveyQuestion(TestCase):
    def setUp(self):
        survey_question.objects.create(question="What is your favorite color", answer="Y")
        

    def test_survey_question_creation(self):
        q = survey_question.get("What is your favorite color")
        self.assertEqual(q.question, "What is your favorite color")
        self.assertEqual(q.answer, "Y")

class Survey(TestCase):
    def setUp(self):
        sq = survey_question(question="Should this test break?", answer="N")
        user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        survey.objects.create(survey_question=sq, user=user)

    def test_survey_creation(self):
        user = User.objects.get(username='jacob')
        s = survey.objects.get(user=user)

        self.assertEqual(s.survey_question.question, "Should this test break?")

