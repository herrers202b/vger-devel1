from django.db import models
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Survey(models.Model):
    """
    Survey Model

    This model is used to represent the metadata about a 
    whole survey

    TODO: Impliment versioning because the various models
    will depend on the state of this post filling of a survey
    """
    titleOfSurvey = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    surveySlug = models.SlugField(null=False, unique=True)


    def save(self, *args, **kwargs):
        """Saves the surveySlug as the titleOfSurvey"""
        if not self.surveySlug:
            self.surveySlug = slugify(self.titleOfSurvey)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("survey-detail", kwargs={'surveySlug': self.surveySlug})
    
    def get_gen_url(self):
        """Returns the generate survey view to prep the users info before taking the survey"""
        return reverse("gen-survey", kwargs={'surveySlug' : self.surveySlug})
    
    def get_take_url(self):
        """Returns the take survey view to send the user from the welcome page to the first page of the survey"""
        return reverse("take-survey", kwargs={'surveySlug' : self.surveySlug, 'page' : 0})


class Category(models.Model):
    """
    Category Model

    Holds the title of the category and a reference to its 
    appropriate survey

    """
    titleOfCategory = models.CharField(max_length=100)
    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)

    
class Survey_Question(models.Model):
    """
    Survey_Question Model

    This model is to be used for answer referencing holding
    a foriegn key of survey, category, and question

    """
    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)
    category_fk = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    question_fk = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)


class Answer(models.Model):
    """
    Answer Model

    This model holds a instance of each answer the user provides
    when taking a survey and holds the user as a foreignkey
    To reference the survey_question foreign key so we can
    evaluate the properties of the question later

    """
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    survey_question_fk = models.ForeignKey('Survey_Question', on_delete=models.CASCADE)
    
    answer_text = models.CharField(max_length=20)


class Question(models.Model):
    """
    Question Model

    used for holding the question_text for the question
    in general. 

    @input_type: used for distinguishing the how
    the answer in the question is to be used for evaluation.
    Ex: Text, Radio, Range?
    
    @option_group: used for a collection of options pre-established
    options based on the input type

    @question_text holds the general question

    @answer_is_required is used to declare wether or not
    the answer is required (TODO impl usage) 

    @is_multi_option_answer is used for question evalutation (TODO impl usage) 
    """
    input_type_fk = models.ForeignKey('Input_Type', on_delete=models.PROTECT)
    option_group = models.ForeignKey('Option_Group', on_delete=models.PROTECT)

    question_text = models.CharField(max_length=200)
    answer_is_required = models.BooleanField()
    is_multi_option_answer = models.BooleanField()


class Option_Group(models.Model):
    """
    Option_Group Model

    @name_of_group: group that holds each of the option_choices in
    a foriegn key
    """
    name_of_group = models.CharField(max_length=20)


class Option_Choice(models.Model):
    """
    Option_Choice Model

    @option_group: holds a foreign key to the name of the group
    of options

    @choice_text: holds the text of the answer to be selected
    or filled
    """
    option_group = models.ForeignKey('Option_Group', on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=20)


class Input_Type(models.Model):
    """
    Input_Type Model

    @input_type_name: holds the type of input like text
    or radio
    """
    input_type_name = models.CharField(max_length=20)


class User_Survey(models.Model):
    """
    User_Survey

    This model is used to keep track of what surveys the user has
    taken TODO: or is in the middle of taking

    @finished: Used for session handling in determining
    wether or not the user has finished the survey

    @user_fk: Holds the user that has taken the survey

    @survey_fk: Holds the survey the user is taking
    """
    finished = models.BooleanField(default=False)     
    
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)
    