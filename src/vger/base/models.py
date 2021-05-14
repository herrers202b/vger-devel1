from django.db import models
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.dispatch import receiver

class Survey(models.Model):
    """
    Survey Model

    This model is used to represent the metadata about a
    whole survey

    TODO: Impliment versioning because the various models
    will depend on the state of this post filling of a survey

    titleOfSurvey : CharField
        the title of the survey

    description : CharField
        a short 100 char length description of this survey

    start_date, end_date : DateTimeField
        the state and end date, respectivly, of this survey

    is_open : BooleanField
        boolean that determines whether or not a survey is live

    surveySlug : SlugField
        a slugfield derived from the title fo the survey, used for url pathing
    """
    titleOfSurvey = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    surveySlug = models.SlugField(null=False, unique=True)
    version_number = models.DecimalField(max_digits=5, decimal_places=2, default=0, unique=True)

    def __str__(self):
        return "V" + str(self.version_number)

    def save(self, *args, **kwargs):
        """Saves the surveySlug as the titleOfSurvey"""
        if not self.surveySlug:
            self.surveySlug = slugify(self.titleOfSurvey + str(self.version_number))
        return super().save(*args, **kwargs)

    def get_new_version_url(self):
        return reverse("new-version", kwargs={'surveySlug': self.surveySlug, 'version_number' : str(self.version_number)})

    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("survey-detail", kwargs={'surveySlug': self.surveySlug})

    def get_welcome_url(self):
        """Returns the url to access the welcome page for this survey"""
        return reverse("welcome-to-survey", kwargs={'surveySlug' : self.surveySlug})

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

    titleOfCategory : CharField
        title of the category with 100 char limiter

    survey_fk : ForeignKey
        the foreign key that is used to access a parent survey
    """
    titleOfCategory = models.CharField(max_length=100)
    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={'surveySlug': self.survey_fk.surveySlug,
                                                    'pk': self.pk})

class Survey_Question(models.Model):
    """
    Survey_Question Model

    This model is to be used for answer referencing holding
    a foriegn key of survey, category, and question


    survey_fk : ForeignKey
        Foreign key used to access a parent survey

    category_fk : ForeignKey
        Foreign key used to access a parent category

    question_fk : ForeignKey
        Foreign key used to access a child question
    """

    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)
    category_fk = models.ForeignKey('Category', related_name = "my_questions", on_delete=models.CASCADE, null=True)
    question_fk = models.ForeignKey('Question', related_name="survey_questions", on_delete=models.CASCADE, null=True)


class Answer(models.Model):
    """
    Answer Model

    This model holds a instance of each answer the user provides
    when taking a survey and holds the user as a foreignkey
    To reference the survey_question foreign key so we can
    evaluate the properties of the question later

    user_fk : ForeignKey
        Foreign key used to access a user

    survey_question_fk : ForeignKey
        Foreign key used to access a Survey Question Object

    answer_text : CharField
        20 chararacter lenght answer text field
    """
    user_survey_fk = models.ForeignKey('User_Survey', on_delete=models.CASCADE, null=True)
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

    option_group = models.ForeignKey('Option_Group', on_delete=models.PROTECT, null=True)
    input_type_fk = models.ForeignKey('Input_Type', on_delete=models.PROTECT)
    question_text = models.CharField(max_length=200)
    answer_is_required = models.BooleanField()
    is_multi_option_answer = models.BooleanField()

    def get_absolute_url(self):
        my_survey_question = Survey_Question.objects.get(question_fk=self.pk)
        my_category = Category.objects.get(pk=my_survey_question.category_fk.pk)
        my_survey = Survey.objects.get(pk=my_survey_question.survey_fk.pk)
        return reverse('question-detail', kwargs={'surveySlug': my_survey.pk,
                                                    'categoryPk': my_category.pk,
                                                    'pk': self.pk,})


class Option_Group(models.Model):
    """
    Option_Group Model

    @name_of_group: group that holds each of the option_choices in
    a foriegn key
    """

    name_of_group = models.CharField(max_length=20)

    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("option-detail", kwargs={'pk': self.pk})

class Option_Choice(models.Model):
    """
    Option_Choice Model

    @option_group: holds a foreign key to the name of the group
    of options

    @choice_text: holds the text of the answer to be selected
    or filled
    """
    OPTION_CHOICE_WEIGHTS = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    )
    option_group = models.ForeignKey('Option_Group', related_name="my_choices", on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=20)
    weight = models.IntegerField(choices=OPTION_CHOICE_WEIGHTS)

class Input_Type(models.Model):
    """
    Input_Type Model

    @input_type_name: holds the type of input like text
    or radio
    """
    INPUT_TYPE_CHOICES = (
        ('text', "Text"),
        ('range', "Range"),
        ( 'tf',"True/False")
    )
    input_type_name = models.CharField(max_length=20, choices=INPUT_TYPE_CHOICES)


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
    time_stamp = models.DateTimeField(auto_now_add=True)

    def get_result_url(self):
        """Returns the results page view to send the user from the take survey page to the results page"""
        return reverse("results-page", kwargs={'surveySlug' : self.survey_fk.surveySlug, 'pk': self.pk})


#NOT FOR CALLING!
@receiver(models.signals.post_delete, sender=Survey_Question)
def delete_reverse(sender, **kwargs):
    """
    delete_reverse

    This functions purpose is intended to delete the Question model
    upon deleting the Survey without using the Survey_Question as
    a foreign key in the Question model

    """
    try:
        if kwargs['instance'].question_fk:
            kwargs['instance'].question_fk.delete()
    except:
        pass



       
    