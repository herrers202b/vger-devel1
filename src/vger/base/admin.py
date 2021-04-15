from django.contrib import admin
# from .models import Question, Category, Survey, SurveyInstance
from .models import Input_Type, Option_Choice, Option_Group, Survey, Survey_Question, Category, Question, Answer
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

class CategoryAdmin(admin.ModelAdmin):
    """
    CategoryAdmin class
    
    This calss allows us to utilize prepopulated_fields
    to automatically generate slugs when a form is filled
    out.
    """
    list_display = ('titleOfCategory',)
#     prepopulated_fields = {'categorySlug': ('titleOfCategory',)}

class QuestionAdmin(admin.ModelAdmin):
    """
    QuestionAdmin class
    
    This calss allows us to utilize prepopulated_fields
    to automatically generate slugs when a form is filled
    out.
    """
    list_display = ('question_text',)
#     prepopulated_fields = {'questionSlug': ('questionNumber',)}

# #Registering above Admin classes and thier respective classes

class Option_GroupAdmin(admin.ModelAdmin):
    """
    QuestionAdmin class
    
    This calss allows us to utilize prepopulated_fields
    to automatically generate slugs when a form is filled
    out.
    """
    list_display = ('name_of_group',)

class Option_ChoiceAdmin(admin.ModelAdmin):
    """
    QuestionAdmin class
    
    This calss allows us to utilize prepopulated_fields
    to automatically generate slugs when a form is filled
    out.
    """
    list_display = ('choice_text', 'option_group',)

class Input_TypeAdmin(admin.ModelAdmin):
    """
    QuestionAdmin class
    
    This calss allows us to utilize prepopulated_fields
    to automatically generate slugs when a form is filled
    out.
    """
    list_display = ('input_type_name',)
admin.site.register(Answer)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Survey_Question)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option_Choice, Option_ChoiceAdmin)
admin.site.register(Option_Group, Option_GroupAdmin)
admin.site.register(Input_Type, Input_TypeAdmin)