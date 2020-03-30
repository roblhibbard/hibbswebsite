# Generated by Django 3.0.3 on 2020-03-27 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_score', models.CharField(blank=True, help_text='Student Test Score', max_length=255, null=True, verbose_name='Student Test Score')),
                ('project_score', models.CharField(blank=True, help_text='Student Project Score', max_length=255, null=True, verbose_name='Student Project Score')),
                ('assignment_score', models.CharField(blank=True, max_length=255, null=True, verbose_name='Student Assignment Score')),
                ('pass_mark', models.CharField(blank=True, max_length=255, null=True, verbose_name='Pass Mark')),
                ('total_marks', models.CharField(blank=True, help_text="Grade's Total Mark", max_length=255, null=True, verbose_name="Grade's Pass Mark")),
                ('student_total_score', models.CharField(blank=True, help_text='Student Total Mark', max_length=255, null=True, verbose_name='Student Total Mark')),
                ('date_score_added', models.DateTimeField(auto_now_add=True)),
                ('date_score_updated', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_grade', to='courses.Course')),
                ('students', models.ManyToManyField(to='students.StudentProfile')),
            ],
        ),
    ]