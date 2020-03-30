# Generated by Django 3.0.3 on 2020-03-30 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_course_students'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('is_enrolled', models.BooleanField(default=True)),
                ('is_unenrolled', models.BooleanField(default=False)),
                ('course_enrolled', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='student', to='courses.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_enrolled', to='students.StudentProfile')),
            ],
        ),
    ]