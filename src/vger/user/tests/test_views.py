from django.test import TestCase, Client
from django.urls import reverse
from ..models import

#=======================================================================

#Try to import the advisor model from models.py
try:
    from ..models import Advisor
except ImportError:
    raise ImportError("The Question model is not implemented for testing import!")

#Try to import the student model from models.py
try:
    from ..models import Student
except ImportError:
    raise ImportError("The Category model is not implemented for testing import!")

#Try to import the admin model from models.py
try:
    from ..models import Administrator
except ImportError:
    raise ImportError("The Survey model is not implemented for testing import!")

class TestViews(TestCase)
