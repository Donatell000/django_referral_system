from django.urls import path

from accounts.views.auth import RequestCodeView, VerifyCodeView
from accounts.views.profile import UserProfileView, ActivateInviteCodeView


urlpatterns = [
    path("auth/request-code/", RequestCodeView.as_view(), name="request-code"),
    path("auth/verify-code/", VerifyCodeView.as_view(), name="verify-code"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/activate-invite/", ActivateInviteCodeView.as_view(), name="activate-invite"),
]
