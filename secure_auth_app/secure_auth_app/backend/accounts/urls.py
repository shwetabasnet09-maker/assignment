from django.urls import path
from .views import RegisterView, LoginView, MFASetupView, MFAVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('mfa/setup/', MFASetupView.as_view()),
    path('mfa/verify/', MFAVerifyView.as_view()),
]

