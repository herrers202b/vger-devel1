from django.test import TestCase, Client
from django.urls import reverse
from ..models import

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

class TestViews(TestCase)
