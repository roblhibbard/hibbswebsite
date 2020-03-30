"""hibbswebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# serve media files
# serve media files
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from hibbswebsite.views import HomePageView
from hibbswebsite.views import SupportPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="main_home"),
    path('support/', SupportPageView.as_view(), name="support"),
    path('admin/', admin.site.urls),
    path('students/', include('students.urls', namespace='students_profile')),
    path('teachers/', include('teachers.urls', namespace='teacher_profile')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('login', include('accounts.urls', namespace='account')),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='dashboard'),
    path('accordion/', TemplateView.as_view(template_name='accordion.html'), name='accordion'),
    # Templates
    path('alert/', TemplateView.as_view(template_name='alert.html'), name='alert'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
