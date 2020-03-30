from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.
from courses.models import Course

User = get_user_model()

GENDER = (
    ('male', "Male"),
    ('female', "Female"),
    ('other', 'Rather Not Mention')
)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    first_name = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        help_text='Student First Name'
    )
    other_name = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        help_text='Student Middle Name'
    )
    last_name = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        help_text='Student Last Name'
    )
    mugshot = models.ImageField(upload_to='student/image/%Y/%m/%d', blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        default='male',
        help_text="Student's Gender"
    )

    date_of_birth = models.DateField(
        auto_now_add=False,
        help_text='Format: YYYY-MM-DD'
    )
    date_admitted = models.DateField(
        auto_now_add=False,
        help_text='Format: YYYY-MM-DD'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(auto_now=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = "Student's Profile"

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.other_name, self.last_name)

    def get_absolute_url(self):
        return reverse("students_profile:student_profile_detail", args=[self.id])


class CourseEnrollment(models.Model):
    """Represents a Student's Enrollment record for a single Course. You should
    generally not manipulate CourseEnrollment objects directly, but use the
    classmethods provided to enroll, unenroll, or check on the enrollment status
    of a given student."""
    MODEL_TAGS = ['course', 'is_active']
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='course_enrolled')

    course_enrolled = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='student')

    date_created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    is_enrolled = models.BooleanField(default=True)
    is_unenrolled = models.BooleanField(default=False)

    def __str__(self):
        return self.student

    def get_absolute_url(self):
        return reverse('students_profile:student_profile_detail', kwargs={'pk': self.pk})

    @classmethod
    def get_or_create_enrollment(cls, student, course_enrolled):
        enrollment, __ = cls.objects.get_or_create(
            user=student,
            course_id=course_enrolled.pk,
            defaults={
                'is_active': False
            }
        )

        return enrollment

    @classmethod
    def update_enrollment(cls, is_active=None):
        """
        Updates an enrollment for a user in a class.  This includes options
        like changing the mode, toggling is_active True/False, etc.
        Also emits relevant events for analytics purposes.
        This saves immediately.
        """

        # if is_active is None, then the call to update_enrollment didn't specify
        # any value, so just leave is_active as it is

        if cls.is_active != is_active and is_active is not None:
            cls.is_active = is_active

    @classmethod
    def add_enrollment(cls, user, course, is_active=True):
        enrollment = cls.add_enrollment(user, course, is_active)

        return enrollment

