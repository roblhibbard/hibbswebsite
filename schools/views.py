# Create your views here.
from datetime import timedelta

from django.shortcuts import render
from django.views.generic import TemplateView

from schools.models import DAYS_OF_WEEK

time_slots = (
    ('7:42 - 9:13', '7:42 - 9:13'),
    ('9:17 - 10:49', '9:17 - 10:49'),
    ('10:49 - 11:29', '10:49 - 11:29'),
    ('11:33 - 1:04', '11:33 - 1:04'),
    ('1:08 - 2:39', '1:08 - 2:39'),
)
t = (
    '9:00 - 9:45', '10:00 - 10:45', '10:45 - 11:55', '12:00 - 12:45', '1:00 - 1:45'
)


class DefaultCoursePeriodView(TemplateView):
    template_name = 'manage/default_timetable.html'

    day_start = timedelta(hours=7, minutes=37)
    class_period = timedelta(minutes=91)
    class_period_special = timedelta(minutes=64)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period_1'] = t[0]
        context['period_2'] = t[1]
        context['lunch'] = t[2]
        context['period_3'] = t[3]
        context['period_4'] = t[4]

        return context


class HomePageScheduleView(TemplateView):
    template_name = 'manage/schedule_small.html'

    day_start = timedelta(hours=7, minutes=37)
    class_period = timedelta(minutes=91)
    class_period_special = timedelta(minutes=64)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period_1'] = t[0]
        context['period_2'] = t[1]
        context['lunch'] = t[2]
        context['period_3'] = t[3]
        context['period_4'] = t[4]

        return context


class StudentScheduleView(TemplateView):
    template_name = 'schedule.html'

    day_start = timedelta(hours=7, minutes=37)
    class_period = timedelta(minutes=91)
    class_period_special = timedelta(minutes=64)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period_1'] = t[0]
        context['period_2'] = t[1]
        context['lunch'] = t[2]
        context['period_3'] = t[3]
        context['period_4'] = t[4]

        return context


def timetable(request):
    matrix = [['' for i in range(7)] for j in range(5)]
    d = dict(DAYS_OF_WEEK)
    t = dict(time_slots)
    for key in d:
        key = key
        print(key)
    for p in t:
        p = p
        print(p)

    context = {'matrix': matrix,
               'd': d,
               'p': p
               }

    return render(request, 'manage/timetable.html', context)
