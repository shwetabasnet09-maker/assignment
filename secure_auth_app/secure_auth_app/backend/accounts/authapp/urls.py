from django.urls import path
from .views import RegisterView, LoginView, MFASetupView, MFAVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('mfa/setup/', MFASetupView.as_view(), name='mfa_setup'),
    path('mfa/verify/', MFAVerifyView.as_view(), name='mfa_verify'),
]
