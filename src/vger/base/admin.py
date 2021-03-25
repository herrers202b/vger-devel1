from django.contrib import admin
from .models import Question, Category, Survey, SurveyInstance

# Register your models here.
admin.site.register(SurveyInstance)



class SurveyAdmin(admin.ModelAdmin):
    list_display = ('titleOfSurvey', 'directions',)
    prepopulated_fields = {'surveySlug': ('titleOfSurvey',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('titleOfCategory',)
    prepopulated_fields = {'categorySlug': ('titleOfCategory',)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questionNumber', 'questionText',)
    prepopulated_fields = {'questionSlug': ('questionNumber',)}

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)