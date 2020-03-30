from django.views.generic import TemplateView
from django.http import HttpResponse


class HomePageView(TemplateView):
    template_name = 'main_home.html'

class SupportPageView(TemplateView):
    template_name = 'support.html'


