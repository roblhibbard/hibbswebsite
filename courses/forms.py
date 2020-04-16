from django.forms.models import inlineformset_factory

from django import forms

from courses.models import Assignment, Course, Module

ModuleFormset = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    extra=2,
    can_delete=True
)


class AssignmentCreateViewForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
