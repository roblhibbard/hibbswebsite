from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
time_slots = (
    ('7:42 - 9:13', '7:42 - 9:13'),
    ('9:17 - 10:49', '9:17 - 10:49'),
    ('10:49 - 11:29', '10:49 - 11:29'),
    ('11:33 - 1:04', '11:33 - 1:04'),
    ('1:08 - 2:39', '1:08 - 2:39'),
)

time_slots_wed = (
    ('7:42 - 8:46', '7:42 - 8:46'),
    ('8:50 - 9:25', '8:50 - 9:25'),
    ('9:29 - 10:33', '9:29 - 10:33'),
    ('10:33 - 11:13', '10:33 - 11:13'),
    ('11:17 - 12:21', '11:17 - 12:21'),
    ('12:25 - 1:39', '12:25 - 1:39'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)


class SchoolProfile(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)
    number_of_students = models.PositiveIntegerField(default=0)
    number_of_staff = models.PositiveIntegerField(default=0)
    address = RichTextField(blank=True, null=True)
    date_school_was_created = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "School's Profile"
        ordering = ('name',)

    def __str__(self):
        return "{} - {}".format(self.name, self.email)



def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


# Triggers
class DefaultPeriods(models.Model):
    rotation_days = {
        ('A', "A-Day"),
        ('B', "B-Day"),
    }

    course_period = {
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
    }
