from django.contrib.auth.models import User
from django.test import TestCase

#=======================================================================

#Try to import the Admin model from models.py
try:
    from ..models import Admin
except ImportError:
    raise ImportError("The Admin model is not implemented for testing import!")

#Try to import the Advisor model from models.py
try:
    from ..models import Advisor
except ImportError:
    raise ImportError("The Advisor model is not implemented for testing import!")

#Try to import the Student model from models.py
try:
    from ..models import Student
except ImportError:
    raise ImportError("The Student model is not implemented for testing import!")

#=======================================================================

#| These section of tests are used for as an extentsion of the user model by including
# each type in a one to one field. Upon creation of the user in a register form you should
# decode which user type is being registered and create the appropriate model object
# 
# |#

class AdminTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="jacob", password="top_secret")
        Admin.objects.create(user=user)

    def test_admin_creation(self):
        user = User.objects.get(username='jacob')
        getAdmin = Admin.objects.get(user=user)

        self.assertEqual(getAdmin.password, "top_secret")



class AdvisorTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="carly", password="top_secret")
        Advisor.objects.create(user=user)

    def test_advisor_creation(self):
        user = User.objects.get(username='carly')
        getAdvisor = Advisor.objects.get(user=user)
    
        self.assertEqual(getAdvisor.password, "top_secret")



class StudentTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="martha", password="top_secret")
        Student.objects.create(user=user)

    def test_student_creation(self):
        user = User.objects.get(username='martha')
        getStudent = Student.objects.get(user=user)

        self.assertEqual(getStudent.password, "top_secret")

