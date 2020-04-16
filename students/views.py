from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    DeleteView,
    CreateView)
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

from accounts.forms import UserCreateForm
from .models import StudentProfile, AttendanceTotal, Attendance
from accounts.models import User
from courses.forms import ModuleFormset
from courses.models import Course, CourseEnrollment, Assign
from courses.utils_mixins import CourseIDMixin
from teachers.models import TeacherProfile
from .forms import (
    StudentProfileCreateForm, CourseEnrollmentFormSet)


def register(request):
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST)
        profile_form = StudentProfileCreateForm(
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.student = True
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user  # set the user created to the profile
            if 'mugshot' in request.FILES:
                profile.mugshot = request.FILES['mugshot']
            profile.save()
            return HttpResponseRedirect(reverse('students_profile:student_profile_list'))
    else:
        user_form = UserCreateForm()
        profile_form = StudentProfileCreateForm()
    return render(request, 'students/profile/create_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class StudentListProfileView(ListView):
    model = StudentProfile
    context_object_name = 'students'
    template_name = 'students/students_list/list.html'
    ordering = ['-last_name']


class StudentDetailProfileView(DetailView):
    model = StudentProfile
    context_object_name = 'student_details'
    template_name = 'students/profile/dashboard.html'


class StudentUpdateProfileView(generic.edit.UpdateView):
    model = StudentProfile
    template_name = 'students/profile/profile_form.html'
    form_class = StudentProfileCreateForm

    # def get_success_url(self):
    #     return HttpResponseRedirect(reverse('students_profile:student_profile_detail', args=[self.object.id]))


class StudentDeleteProfileView(DeleteView):
    model = StudentProfile
    success_url = reverse_lazy('students_profile:student_profile_list')
    template_name = 'students/profile/delete.html'


# Course Students Are Enrolled in
class StudentCourseList(LoginRequiredMixin, ListView):
    model = CourseEnrollment
    template_name = 'students/course/list.html'


class StudentEnrollCourseView(TemplateResponseMixin, View):
    template_name = 'students/manage/enrollments/enroll.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormset(instance=self.course, data=data)

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.course = get_object_or_404(Course, id=pk, owner=TeacherProfile.objects.get(user=self.request.user))
        return super(StudentEnrollCourseView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return reverse_lazy('student_course_detail',
                                args=[self.course.id])
        return self.render_to_response({
            'course': self.course,
            'formset': formset
        })


def self(kwargs):
    pass


def student_enroll(request):
    template_name = 'students/manage/enrollments/enroll.html'

    if request.method == 'GET':
        formset = CourseEnrollmentFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = CourseEnrollmentFormSet(request.POST)

    return render(request, template_name, {
        'formset': formset,
    })


class CourseEnrollmentViewMixin(object):
    model = Course

    def get_success_url(self):
        return reverse_lazy('course', kwargs={'sec': self.kwargs['course']})


class CourseEnrollmentCreateView(LoginRequiredMixin, CreateView):
    course = None
    user = None
    template_name = 'students/manage/enrollments/courseenrollment_form.html'
    fields = ['user', 'course']
    model = CourseEnrollment

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.user = form.cleaned_data['user']

        print(self.course.pk)
        print(self.user.pk)
        return super(CourseEnrollmentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students_profile:student_course_detail_view', args=[self.user.pk, self.course.pk])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    context_object_name = 'module'

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        print(course)
        if 'module_id' in self.kwargs:
            print(self.kwargs)
            # get current module
            context['module'] = course.modules.get(
                                    id=self.kwargs['module_id'])
            print(context['module'])
            print('in module_id')
        else:
            # get first module
            context['module'] = course.modules.all()[0]
            print('not in module_id')
        return context


def attendance(request, stud_id):
    stud = StudentProfile.objects.get(USN=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'students/manage/attendance/attendance.html', {'att_list': att_list})


def attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(StudentProfile, USN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/att_detail.html', {'att_list': att_list, 'cr': cr})


def upload_student(request):
    '''
    View for uploading Students
    '''
    # quiz = get_object_or_404(Quiz,slug=quiz_slug)
    template_name = 'students/profile/upload.html'
    if request.method == 'POST':
        csvfile = request.FILES['studentprofile']  # gets the input field name
        print(csvfile.name)  # prints the csv file name
        if not csvfile.name.endswith('.csv'):
            print("Invalid!!")  # prints invalid at the console
            messages.error(request, "CSV file format not supported")
            return (HttpResponseRedirect('studentprofile:fail'))
        file_data = csvfile.read().decode("utf-8")  # reads the csv file
        # print(file_data)
        lines = file_data.split("\n")  # split using the delimiter
        data_dict = {}  # empty dictionary to store the csv data
        print(len(lines))
        for line in lines:
            print(line)
            fields = line.split(',')
            # print(fields)
            user_dict = {
                'email': fields[0],
                'password': fields[1],
                # 'password2':fields[2],
            }
            student_profile_dict = {
                'first_name': fields[2],
                'other_name': fields[3],
                'last_name': fields[4],
                'gender': fields[5],
                'mugshot': fields[6],

                'date_of_birth': fields[7],
                'date_admitted': fields[8],
                'address': fields[9]
            }
            # print(len(data_dict))
            if data_dict != '':
                user = User.objects.create_user(
                    email=user_dict['email'],
                    password=user_dict['password']
                )
                user.student = True
                user.save()  # save the user
                student_profile = StudentProfile.objects.create(
                    user=user,
                    first_name=student_profile_dict['first_name'],
                    other_name=student_profile_dict['other_name'],
                    last_name=student_profile_dict['last_name'],
                    mugshot=student_profile_dict['mugshot'],
                    gender=student_profile_dict['gender'],

                    date_of_birth=student_profile_dict['date_of_birth'],
                    date_admitted=student_profile_dict['date_admitted'],
                    address=student_profile_dict['address']
                )
                messages.success(request, "File Successfully Uploaded")
            else:
                messages.error(request, "File not uploaded")
    context = {}
    return render(request, template_name, context)
