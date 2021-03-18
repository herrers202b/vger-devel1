from django.contrib import admin
from .models import Question, Category, Survey, SurveyInstance

# Register your models here.
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Survey)
admin.site.register(SurveyInstance)