from django.db import models
from django.contrib.auth.models import User

# Advisor model: Can view completed surveys of only their advisees
class Advisor(models.Model): 
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Student model: exists to create a relationship between advisors and advisees
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, null=False)

# Administrator model: Model for use for user accounts to have survey edit
# access, separate from site backend administration
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
