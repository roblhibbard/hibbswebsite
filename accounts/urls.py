from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('register/', views.SignUp.as_view(), name='register'),
]   
