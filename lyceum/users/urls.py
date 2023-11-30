from django.urls import path

import users.views
import django.contrib.auth.views


app_name = "users"


urlpatterns = [
    path(
        "user_list/",
        users.views.user_list,
        name="user_list",
    ),
    path(
        "user_detail/<int:pk>/",
        users.views.user_detail,
        name="user_detail",
    ),
    path(
        "signup/",
        users.views.signup,
        name="signup",
    ),
    path(
        "activate/<str:name>",
        users.views.activate,
        name="signup",
    ),
    path(
        "login/",
        users.views.login,
        name="login",
    ),
    path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(),
        name="reset_confirm",
    ),
    path(
        "reset/done/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(),
        name="reset_done",
    ),
]
