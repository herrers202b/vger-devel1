from django.contrib import admin
from .models import Question, Category, Survey

# Register your models here.
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Survey)