from django.db import models
#Used to generate URLs by reversing the URL patterns
from django.urls import reverse
import uuid
from django.template.defaultfilters import slugify

import hashlib, random, sys
from django.contrib.auth.models import User
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
    ansser : int 
        answer will be the selected weight for our question or prompt, should
        be on a scale of 0-4
    QUESTION_WEIGHTS : choice
        QUESTION_WEIGHTS will be a choice/radio button that allows the user
        to select from 0 to 4 on a scale of weights for some questionText
    category : forign key
        category is our forign key to the category model.
         Used to link questions to categories
    questionNumber : int
        the number of the question the user will be adding to
        the catergory
    questionSlug : slugField
        this is our unique slug that we will use to create URLs from 
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
    answer = models.IntegerField(choices=QUESTION_WEIGHTS, blank=True, null=True, help_text="Results of question")
    category = models.ForeignKey("Category", verbose_name=("Parent Category"), related_name=("questions"), default=None, null=True, on_delete=models.CASCADE)
    questionNumber = models.IntegerField(default='1', help_text="Please enter a question number")
    questionSlug = models.SlugField(null=False, unique=True)


    """String for representing the Question object."""
    def __str__(self):
        return f'{self.questionNumber}'

    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("question-detail", kwargs={'questionSlug': self.questionSlug,
                                                    'categorySlug': self.category.categorySlug,
                                                    'surveySlug': self.category.survey.surveySlug})

    def save(self, *args, **kwargs):
        if not self.questionSlug:
            hash = hashlib.sha1()
            hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
            self.questionSlug = slugify(hash.hexdigest())
        return super().save(*args, **kwargs)

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
    categorySlug : slugField
        this is our unique slug that we will use to create URLs from 
    """
    titleOfCategory = models.CharField(max_length=100, help_text="Please enter a title for this category, ex) Computer Skills.")
    lowWeightText = models.CharField(max_length=50, default="Not like me at all", help_text="Please enter flavor text for the low weight of the category, ex) Not like me at all")
    highWeightText = models.CharField(max_length=50, default="Extremely like me", help_text="Please enter flavor text for the high weight of the category, ex) Extremely like me")
    survey = models.ForeignKey("Survey", verbose_name=("Parent Survey"), related_name=("categories"), default=None, null=True, on_delete=models.CASCADE)
    categorySlug = models.SlugField(null=False, unique=True)

    """String for representing the Category object."""
    def __str__(self):
        return f'{self.titleOfCategory}'
    
    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("category-detail", kwargs={'categorySlug': self.categorySlug,
                                                    'surveySlug': self.survey.surveySlug})

    def save(self, *args, **kwargs):
        if not self.categorySlug:
            self.categorySlug = slugify(self.titleOfCategory)
        return super().save(*args, **kwargs)
    
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
    created : DateTimeField
        created is a timestamp for the date the survey was created
    lastUpdated : DateTimeField  
        lastUpdated is a timestamp for the last time a save() call
        was made in this model
    surveySlug : slugField
        this is our unique slug that we will use to create URLs from 
    """
    
    titleOfSurvey = models.CharField(max_length=50, help_text="Please enter a name for the survey")
    directions = models.CharField(max_length=500, help_text="Please enter any directions to take the survey")
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    surveySlug = models.SlugField(null=False, unique=True)

    #This is to discern wether the model is being used as a template to take or a survey being taken 
    assigned = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    """String for representing the Survey object."""
    def __str__(self):
        return f'{self.titleOfSurvey}'
    
    #Replacing pk with slug for tutorial go here:
    #https://learndjango.com/tutorials/django-slug-tutorial
    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("survey-detail", kwargs={'surveySlug': self.surveySlug})
    
    def get_creation_url(self):
        return reverse("gen-survey", args=[str(self.pk)])

    def save(self, *args, **kwargs):
        if not self.surveySlug:
            self.surveySlug = slugify(self.titleOfSurvey)
        return super().save(*args, **kwargs)
    


#Untested survey instance model
class SurveyInstance(models.Model):
    @staticmethod
    def create_session_hash():
            hash = hashlib.sha1()
            hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
            return hash.hexdigest()  
    """
    SurveyInstance model

    The model for a specific instance of a survey

    Parameters
    ----------
    id : UUIDField
        Unique id of the survey instance
    survey : Foriegn Key
        survey is the forign key into a specific survey
        with which we wish to instantiate 
    """
    session_hash = models.CharField(max_length=40, unique=True, default=create_session_hash.__func__)
    survey = models.ForeignKey('Survey', on_delete=models.RESTRICT, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        """String for representing the Survey Instance Object"""
        return f'{self.session_hash})'
    
    def get_welcome_url(self):
        return reverse("welcome-to-survey", args=[str(self.session_hash)])

    def get_absolute_url(self):
        return reverse("take-survey", args=[str(self.session_hash), 0])
    
    def get_exit_url(self):
        return reverse("results-page", args=[str(self.session_hash)])
    
