from django.db import models
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from user.models import customUser
from django.template.defaultfilters import slugify
# Create your models here.

class Survey(models.Model):
    titleOfSurvey = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    surveySlug = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.surveySlug:
            self.surveySlug = slugify(self.titleOfSurvey)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Returns the url to access a detailed record for this survey"""
        return reverse("survey-detail", kwargs={'surveySlug': self.surveySlug})
    
    

class Category(models.Model):
    titleOfCategory = models.CharField(max_length=100)
    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)

    
class Survey_Question(models.Model):
    survey_fk = models.ForeignKey('Survey', on_delete=models.CASCADE)
    category_fk = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    question_fk = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)

class Answer(models.Model):
    user_fk = models.ForeignKey(customUser, on_delete=models.CASCADE)
    survey_question_fk = models.ForeignKey('Survey_Question', on_delete=models.CASCADE)
    
    answer_text = models.CharField(max_length=20)


class Question(models.Model):
    input_type_fk = models.ForeignKey('Input_Type', on_delete=models.PROTECT)
    option_group = models.ForeignKey('Option_Group', on_delete=models.PROTECT)

    question_text = models.CharField(max_length=200)
    answer_is_required = models.BooleanField()
    is_multi_option_answer = models.BooleanField()

class Option_Group(models.Model):
    name_of_group = models.CharField(max_length=20)

class Option_Choice(models.Model):
    option_group = models.ForeignKey('Option_Group', on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=20)

class Input_Type(models.Model):
    input_type_name = models.CharField(max_length=20)
