from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from teachers.models import TeacherProfile
from .fields import OrderField

# Create your models here.

User = get_user_model()


class Subject(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, null=True, help_text='Subject Code')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='courses_created')
    title = models.CharField(max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    slug = models.SlugField(unique=True, blank=True, null=True, help_text='Course Code')
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)
    overview = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('can_enroll', 'Enroll In Course'),
        )

    def __str__(self):
        return "{} created by {}".format(self.title, self.owner)


class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_enrolled')

    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='courses_enrolled')

    date_created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    is_enrolled = models.BooleanField(default=True)

    def __str__(self):
        return self.course.students

    def get_absolute_url(self):
        return reverse_lazy("students_profile:student_profile_detail", args=[self.id])


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    instruction = models.TextField(blank=False)
    date_due = models.DateField()
    date_created = models.DateField(auto_now_add=True, null=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True)

    points_possible = models.IntegerField()

    CATEGORIES = {
        ('essay', "Essay"),
        ('test', "Test"),
        ('quiz', "Quiz"),
        ('ps', "Problem Set"),
        ('hwk', "Homework"),
        ('ec', "Extra Credit")
    }

    category = models.CharField(choices=CATEGORIES, max_length=20)

    def __str__(self):
        return "[" + self.get_assignment_category() + "] " + str(self.title) + ": " + str(self.instruction)

    def get_assignment_category(self):
        return dict(self.CATEGORIES).get(str(self.category))


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, limit_choices_to={
        'model__in': (
            'text',
            'video',
            'image',
            'file'
        )
    })
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('course/content/{}.html'.format(self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='courses/file/%Y/%m/%d')


class Image(ItemBase):
    file = models.FileField(upload_to='courses/images/%Y/%m/%d')


class Video(ItemBase):
    url = models.URLField()
