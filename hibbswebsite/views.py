from datetime import datetime

from django.views.generic import TemplateView

t = (
    '9:00 - 9:45', '10:00 - 10:45', '10:45 - 11:55', '12:00 - 12:45', '1:00 - 1:45'
)


class HomePageView(TemplateView):
    template_name = 'main_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period_1'] = t[0]
        context['period_2'] = t[1]
        context['lunch'] = t[2]
        context['period_3'] = t[3]
        context['period_4'] = t[4]

        return context


class SupportPageView(TemplateView):
    template_name = 'support.html'


class VideoPageView(TemplateView):
    template_name = 'video.html'


class SchedulePageView(TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period_1'] = t[0]
        context['period_2'] = t[1]
        context['lunch'] = t[2]
        context['period_3'] = t[3]
        context['period_4'] = t[4]

        return context

    today = datetime.now()



