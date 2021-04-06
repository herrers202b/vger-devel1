from django.contrib import admin
# from .models import Question, Category, Survey, SurveyInstance
from .models import Survey
# # Register your models here.
# admin.site.register(SurveyInstance)

class SurveyAdmin(admin.ModelAdmin):
    """
    SurveyAdmin class
    
    This calss allows us to utilize prepopulated_fields
    to automatically generate slugs when a form is filled
    out.
    """
    list_display = ('titleOfSurvey', 'description',)
    prepopulated_fields = {'surveySlug': ('titleOfSurvey',)}

# class CategoryAdmin(admin.ModelAdmin):
#     """
#     CategoryAdmin class
    
#     This calss allows us to utilize prepopulated_fields
#     to automatically generate slugs when a form is filled
#     out.
#     """
#     list_display = ('titleOfCategory',)
#     prepopulated_fields = {'categorySlug': ('titleOfCategory',)}

# class QuestionAdmin(admin.ModelAdmin):
#     """
#     QuestionAdmin class
    
#     This calss allows us to utilize prepopulated_fields
#     to automatically generate slugs when a form is filled
#     out.
#     """
#     list_display = ('questionNumber', 'questionText',)
#     prepopulated_fields = {'questionSlug': ('questionNumber',)}

# #Registering above Admin classes and thier respective classes
admin.site.register(Survey, SurveyAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Question, QuestionAdmin)