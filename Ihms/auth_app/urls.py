from django.urls import path
from .views import SignUpView, LoginView,ConfirmUserView

urlpatterns = [
    path('register', SignUpView.as_view(), name='register'),  
    path('login/', LoginView.as_view(), name='login'),  
    path('confirm',ConfirmUserView.as_view(),name='test')         
]
