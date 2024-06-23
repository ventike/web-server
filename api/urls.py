from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserList.as_view(), name="user-view-create"),
    path("usersold/", views.UserListCreate.as_view(), name="user-view-create")
]