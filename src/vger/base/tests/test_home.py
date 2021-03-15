from django.test import RequestFactory, TestCase, SimpleTestCase
from django.urls import reverse, resolve
try:
    from ..views import home
except ImportError:
    raise ImportError("The home view is not implemented for testing import!")

#|HomeTest
#   1. Tests to see if home.html is used and called properly when going to url
#   2. Tests to see if the url resolves properly
# |#


class HomeTest(TestCase):

    def test_template(self):
        self.assertTemplateUsed(self.response, 'home.html')


    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)
