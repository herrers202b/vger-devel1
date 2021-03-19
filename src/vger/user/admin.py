from django.contrib import admin
from .models import Student, Advisor, Administrator

admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(Administrator)
