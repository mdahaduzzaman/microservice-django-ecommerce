from django.urls import path

from accounts.views import UserRolesView


urlpatterns = [
    path("users/<str:user_id>/roles/", UserRolesView.as_view(), name="user-roles"),
]
