from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view()),
    path('register', views.RegisterView.as_view()),
    path('otp', views.OTPView.as_view())
]
