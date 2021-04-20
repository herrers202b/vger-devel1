from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
class Advisor(models.Model): 
    # Advisor model: Can view completed surveys of only their advisees
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='advisorAccount')
    
    class Meta:
        permissions = (('canTakeSurvey', 'can take survey'),
                        ('canViewOwnResults', 'can see own results'),
                        ('canSeeAdviseeSurvey', 'can see advisee survey'),)


class Student(models.Model):
    # Student model: exists to create a relationship between advisors and advisees
    advisor = models.ForeignKey("Advisor", related_name=("Advisee"), default=None, null=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentAccount')

    class Meta:
        permissions = (('canTakeSurvey', 'can take survey'),
                        ('canViewOwnResults', 'can see own results'))

                        
class Administrator(models.Model):
    # Administrator model: Model for use for user accounts to have survey edit
    # access, separate from site backend administration
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adminAccount')
    survey = models.ManyToManyField("base.Survey")
    class Meta:
        permissions = (('canCreateSurvey', 'can create survey'),
                        ('canEditSurvey', 'can edit survey'),
                        ('canDeleteSurvey', 'can delete survey'),
                        ('canCreateCategory', 'can create category'),
                        ('canEditCategory', 'can edit category'),
                        ('canDeleteCategory', 'can delete category'),
                        ('canCreateQuestion', 'can create question'),
                        ('canEditQuestion', 'can edit question'),
                        ('canDeleteQuestion', 'can delete question'),
                        ('canTakeSurvey', 'can take survey'),
                        ('canViewOwnResults', 'can see own results'),
                        ('canCreateUser', 'can create user'),
                        ('canUpdateUser', 'can update user'),
                        ('canDeleteUser', 'can delete user'),
                        ('canSeeSurveyDetail', 'can see survey detail view'),
                        ('canSeeCategoryDetail', 'can see category detail view'),
                        ('canSeeQuestionDetail','can see question detail view'),)
