from django.contrib import admin
from .models import StudentProfile


# Register your models here.

@admin.register(StudentProfile)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('students_name', 'last_name')
    list_filter = ('first_name',)
    order_by = ('-last_name',)

    def students_name(self):
        return '{} {} {}'.format(self.first_name, self.other_name, self.last_name).title()
