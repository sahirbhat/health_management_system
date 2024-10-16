from django.urls import path
from .views import SignUpView, LoginView,ConfirmUserView,ConfirmPasswordResetView,ForgotPasswordView

urlpatterns = [
    path('register', SignUpView.as_view(), name='register'),  
    path('login/', LoginView.as_view(), name='login'),  
    path('confirm',ConfirmUserView.as_view(),name='test'),   
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('password-reset/', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
]      

