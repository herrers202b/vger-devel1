from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

#Try to import the SurveyListView view from views.py
try:
    from ..views import SurveyListView
except ImportError:
    raise ImportError("The SurveyListView view is not implemented for testing import!")

#Try to import the SurveyDetailView view from views.py
try:
    from ..views import SurveyDetailView
except ImportError:
    raise ImportError("The SurveyDetailView view is not implemented for testing import!")

#Try to import the home view from views.py
try:
    from ..views import home
except ImportError:
    raise ImportError("The home view is not implemented for testing import!")

#|Urls Test
#   1. Tests to see if each url is used and called properly when going to url
#   2. Tests to see if the url resolves properly
# |#

class TestUrls(TestCase):

    def test_survey_url(self):
        url = reverse('survey')
        self.assertEquals(resolve(url).func.view_class, SurveyListView)

    def test_survey_detail_url(self):
        url = reverse('survey-detail')
        self.assertEquals(resolve(url).func.views_class, SurveyDetailView)

    # def test_survey_detail_url(self):
    #     resolver = resolve('survey-detail')
    #     self.assertEqual(resolver.func.cls, SurveyDetailView)

    def test_home_page_url(self):
        url = reverse('home-page')
        self.assertEquals(resolve(url).func, home)

    # def test_survey_create_url(self):
    #     url = reverse('survey-create')
    #     self.assertEquals(resolve(url).func.views_class, SurveyCreate)