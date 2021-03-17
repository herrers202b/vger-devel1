from django.db import models
# Create your models here.

#Untested question model
class Question(models.Model):
    """
    Question Model

    The model for our individual questions

    Parameters
    ----------
    questionText : str
        questionText serves as the text of our question or general prompt
    score : int 
        score will be the selected weight for our question or prompt, should
        be on a scale of 0-4
    QUESTION_WEIGHTS : choice
        QUESTION_WEIGHTS will be a choice/radio button that allows the user
        to select from 0 to 4 on a scale of weights for some questionText
    category : forign key
        category is our forign key to the category model.
         Used to link questions to categories
    """
    #Choices bank with weights and questions
    QUESTION_WEIGHTS = (
        (0,'weight 0'),
        (1,'weight 1'),
        (2,'weight 2'),
        (3,'weight 3'),
        (4,'weight 4'),
    )
    questionText = models.CharField(max_length=100, help_text="Please enter a prompt. ex) I know how to install software on my computer.")
    score = models.IntegerField(choices=QUESTION_WEIGHTS, blank=True, null=True, help_text="Results of question")
    category = models.ForeignKey("Category", verbose_name=("Parent Category"), default=None, null=True, on_delete=models.CASCADE)

    """String for representing the Question object."""
    def __str__(self):
        return f'{self.questionText}'
    

#Untested character model
class Category(models.Model):
    """
    Category Model

    The model for categories of questions

    Parameters
    ----------
    titleOfCategory : str
        titleOfCategory will be the title of our category, ex "Computer Skills"
    lowWeightText : str
        lowWeightText flavor text for our lower weight header, ex "Not like me at all"
    highWeightText : str
        highWeightText flavor text for our high weight header, ex "Extremely like me"
    survey : forign key
        survey will be our forign key to the survey model such 
        that we can link categoies of surveys.
    """
    titleOfCategory = models.CharField(max_length=100, help_text="Please enter a title for this category, ex) Computer Skills.")
    lowWeightText = models.CharField(max_length=50, default="Not like me at all", help_text="Please enter flavor text for the low weight of the category, ex) Not like me at all")
    highWeightText = models.CharField(max_length=50, default="Extremely like me", help_text="Please enter flavor text for the high weight of the category, ex) Extremely like me")
    survey = models.ForeignKey("Survey", verbose_name=("Parent Survey"), default=None, null=True, on_delete=models.CASCADE)

    """String for representing the Category object."""
    def __str__(self):
        return f'{self.titleOfCategory}'
    
#Untested survey model
class Survey(models.Model):
    """
    Survey model

    The model for the survey category

    Parameters
    ----------
    titleOfSurvey : str
        titleOfSurvey serves as the title of our survey, ex "VGER"
    directions : str
        directions will allow an admin to write any specific
        directions for their survey 
    """
    titleOfSurvey = models.CharField(max_length=50, help_text="Please enter a name for the survey")
    directions = models.CharField(max_length=500, help_text="Please enter any directions to take the survey")
    
    """String for representing the Survey object."""
    def __str__(self):
        return f'{self.titleOfSurvey}'