from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ContestantCreateView, home, check_answer

urlpatterns = [
    path('', home, name='home'),
    path('check_answer', check_answer, name='check_answer'),
    path('login', auth_views.LoginView.as_view(template_name='hexdle/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', ContestantCreateView.as_view(), name='register'),
]