from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("users/<int:userid>/", detail_user_account),
    path("users/", get_all_users_info),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
    path("change-password/", change_password),
    path("send_email/", request_otp),
    path("check_otp/", enter_otp),
    path("reset_password/", reset_password),
]
