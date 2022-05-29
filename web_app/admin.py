from django.contrib import admin

# Register your models here.
from .models import StudentData
class Student(admin.ModelAdmin):
      list_display    = ('name', 'email', 'roll', 'course', 'stream', 'gender', 'year' , 'present_days', 'total_days')

admin.site.register(StudentData, Student)
