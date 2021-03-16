from django.db import models
#from user import models
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
    
    weights[0-4] : str
        These strings can be either left blank or filled in with specific 
        prompts to the user. This is done to let the admin make a more
        personalized survey question for a given category

    """
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
    question : forign key
        question is our forign key to the question model. Used to link questions to categories
    """
    titleOfCategory = models.CharField(max_length=100, help_text="Please enter a title for this category, ex) Computer Skills.")
    lowWeightText = models.CharField(max_length=50, help_text="Please enter flavor text for the low weight of the category, ex) Not like me at all")
    highWeightText = models.CharField(max_length=50, help_text="Please enter flavor text for the high weight of the category, ex) Extremely like me")
    question = models.ForeignKey("Question", verbose_name=("Question"), on_delete=models.CASCADE)
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
    category : forign key
        category will be our forign key to the category model such 
        that we can link categoies of questions to our survey. 

    Returns
    -------
    int
        Description of return value

    """
    titleOfSurvey = models.CharField(max_length=50, help_text="Please enter a name for the survey")
    directions = models.CharField(max_length=500, help_text="Please enter any directions to take the survey")
    category = models.ForeignKey("Category", verbose_name=("Category"), default=None, on_delete=models.CASCADE)
    #User