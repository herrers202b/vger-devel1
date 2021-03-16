from django.db import models
#from user import models
# Create your models here.
class Question(models.Model):
    #Individual chararacter fields such that admin can create specific
    #questions or statments pertaining to the specific weight
    weight0 = models.CharField("Statement or question", max_length=50)
    weight1 = models.CharField("Statement or question", max_length=50)
    weight2 = models.CharField("Statement or question", max_length=50)
    weight3 = models.CharField("Statement or question", max_length=50)
    weight4 = models.CharField("Statement or question", max_length=50)
    #Choices bank with weights and questions
    QUESTION_WEIGHTS = (
        ('0',weight0),
        ('1',weight1),
        ('2',weight2),
        ('3',weight3),
        ('4',weight4),
    )
    #Text of question or statement being presented
    questionText = models.CharField(max_length=100, help_text="Please enter a prompt. ex) I know how to install software on my computer.")
    #Score attained from radio buttons
    score = models.IntegerField(choices=QUESTION_WEIGHTS, blank=True, default='2', help_text="Results of question")
class Category(models.Model):
    titleOfCategory = models.CharField(max_length=100, help_text="Please enter a title for this category, ex) Computer Skills.")
    lowWeightText = models.CharField(max_length=50, help_text="Please enter flavor text for the low weight of the category, ex) Not like me at all")
    highWeightText = models.CharField(max_length=50, help_text="Please enter flavor text for the high weight of the category, ex) Extremely like me")
    question = models.ForeignKey("Question", verbose_name=("Question"), on_delete=models.CASCADE)
class Survey(models.Model):
    titleOfSurvey = models.CharField(max_length=50, help_text="Please enter a name for the survey")
    directions = models.CharField(max_length=500, help_text="Please enter any directions to take the survey")
    category = models.ForeignKey("Category", verbose_name=("Category"), default=None, on_delete=models.CASCADE)
    #User