from django.views.generic import TemplateView
from datetime import datetime


class HomePageView(TemplateView):
    template_name = 'main_home.html'


class SupportPageView(TemplateView):
    template_name = 'support.html'


class VideoPageView(TemplateView):
    template_name = 'video.html'


class SchedulePageView(TemplateView):
    template_name = 'schedule.html'

    today = datetime.now()
