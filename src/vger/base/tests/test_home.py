from django.test import RequestFactory, TestCase, SimpleTestCase
from django.urls import reverse, resolve
try:
    from ..views import home
except ImportError:
    raise ImportError("The home view is not implemented for testing import!")




class HomeTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)
