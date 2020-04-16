from django.urls import path
from . import views
from .views import DefaultCoursePeriodView

app_name = 'schools'

urlpatterns = [
    path('timetable/', views.timetable, name='timetable'),
    path('timetable/default/', views.DefaultCoursePeriodView.as_view(), name='default_timetable'),
    path('timetable/daily/', views.HomePageScheduleView.as_view(), name='schedule')
]
