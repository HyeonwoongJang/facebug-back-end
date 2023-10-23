from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('register/email-check/', views.EmailCheckView.as_view(), name='email_check_view'),
    path('register/nickname-check/', views.NicknameCheckView.as_view(), name='nickname_check_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('user/info/<int:user_id>/', views.UserInfoView.as_view(), name='user_info_view'),
    path('send-verification-email/', views.SendVerificationEmailView.as_view(), name='send_verification_email_view'),
]