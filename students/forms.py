from django import forms
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from courses.models import Course
from students.models import StudentProfile, CourseEnrollment


class StudentProfileCreateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ('date_created', 'date_updated', 'user')

    def save(self, commit=True):
        user = super(StudentProfileCreateForm, self).save(commit=False)
        if commit:
            user.student = True
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['other_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})

        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_admitted'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})


# Allows the selection of a single model object, suitable for representing a foreign key. Note that the default widget
# for ModelChoiceField becomes impractical when the number of entries increases.
# You should avoid using it for more than 100 items.
#
# A single argument is required:


class CourseEnrollmentForm(forms.ModelForm):
    courses = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple,
                                     queryset=Course.objects.all())
    users = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple,
                                   queryset=StudentProfile.objects.all())

    class Meta:
        model = CourseEnrollment
        fields = ['course_enrolled', 'student']


CourseEnrollmentFormSet = modelformset_factory(CourseEnrollment, exclude=('date_created',))
