from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
# Create your models here.



User = get_user_model()

GENDER = (
    ('male', "Male"),
    ('female', "Female"),
    ('other', 'Rather Not Mention')
)


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300, blank=False, null=False)
    other_name = models.CharField(max_length=300, blank=False, null=False)
    last_name = models.CharField(max_length=300, blank=False, null=False)
    #mugshot = models.ImageField(upload_to='teachers/images/%Y/%m/%d', blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER, default='male')

    # teacher_class = models.CharField(max_length=50, choices=Class_Period, default='')
    # qualification = models.FileField(upload_to='teacher/file/%Y/%m/%d', blank=True, null=True, default='text.txt')
    date_of_birth = models.DateField(
        auto_now_add=False,
        help_text='Format: YYYY-MM-DD'
    )
    date_admitted = models.DateField(
        auto_now_add=False,
        help_text='Format: YYYY-MM-DD'

    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    address = RichTextField(blank=True)

    class Meta:
        verbose_name = "Teacher's Profile"

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.other_name, self.last_name)

    def get_absolute_url(self):
        return reverse("teacher_profile:teacher_profile_detail", args=[self.pk])

