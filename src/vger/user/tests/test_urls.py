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

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, registerPage)

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class, profilePage)

    def test_home_page_url(self):
        url = reverse('home-page')
        self.assertEquals(resolve(url).func, home)