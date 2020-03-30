from django.contrib import admin
from .models import (Grade)

# Register your models here.

class GradeAdmin(admin.ModelAdmin):
    list_display = ('test_score', 'project_score', 'assignment_score', 'pass_mark', 'total_marks', 'student_total_score')


admin.site.register(Grade, GradeAdmin)
