from django.contrib import admin
from .models import (
    Course,
    Subject,
    Module,
    Content,
    Assignment,
    CourseEnrollment,
)


# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('date_created',)
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'subject', 'date_created')
    list_filter = ('date_created', 'subject', 'owner')
    inlines = [ModuleInline]


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'instruction', 'date_due', 'date_created', 'date_updated', 'points_possible', 'category',)
    list_filter = ('date_due',)



admin.site.register(Content)
admin.site.register(CourseEnrollment)

