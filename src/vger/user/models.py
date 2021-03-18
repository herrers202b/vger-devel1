from django.db import models
from django.contrib.auth.models import User

## User Roles

# adm: administrator role, can create and edit surveys
# adv: advisor role, can view advisee survey results
# stu: student role, can take a survey and view their past results
class UserModels(models.Model):
    TYPES = (
        ('adm', 'Administrator'),
        ('adv', 'Advisor'),
        ('stu', 'Student'),
    )

    account_type = models.CharField(max_length=3,choices=TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create(cls, account_type, user):
        inf = cls(account_type=account_type, user=user)
        return inf
      
# Student model: exists to create a relationship between advisors and advisees
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Advisor model: Can view completed surveys of only their advisees
class Advisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advisees = models.ForeignKey(Student, on_delete=models.CASCADE)

# Administrator model: Model for use for user accounts to have survey edit
# access, separate from site backend administration
class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)