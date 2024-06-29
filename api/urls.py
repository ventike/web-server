from django.urls import path
from . import views

urlpatterns = [
    path("private/user/", views.UserData.as_view(), name="user-view-get"),
    path("private/users/", views.UserList.as_view(), name="user-view-list"),
    path("private/login/", views.UserAuthentication.as_view(), name="user-view-login"),
    path("private/create-account/", views.UserCreation.as_view(), name="user-view-create"),
    path("private/modify-user/", views.UserModification.as_view(), name="user-view-modify"),
    path("private/change-password/", views.UserPasswordModification.as_view(), name="user-view-change-password"),
    path("private/delete-user/", views.UserDeletion.as_view(), name="user-view-delete"),
    path("private/partners/", views.PartnerList.as_view(), name="partner-view-list"),
    path("private/create-partner/", views.PartnerCreation.as_view(), name="partner-view-create"),
    path("private/modify-partner/", views.PartnerModification.as_view(), name="partner-view-modify"),
    path("private/delete-partner/", views.PartnerDeletion.as_view(), name="partner-view-delete"),
    path("private/events/", views.EventList.as_view(), name="event-view-list"),
    path("private/create-event/", views.EventCreation.as_view(), name="event-view-create"),
    path("private/modify-event/", views.EventModification.as_view(), name="event-view-modify"),
    path("private/delete-event/", views.EventDeletion.as_view(), name="event-view-delete"),
    path("private/modify-organization/", views.OrganizationModification.as_view(), name="organization-view-modify"),
    path("private/dashboard/", views.DashboardList.as_view(), name="admin-view-list"),
    path("private/admin/", views.AdminList.as_view(), name="admin-view-list"),
    path("private/openai-key/", views.GPTAIYKEY.as_view(), name="openai-key-view-get"),
    # path("usersold/", views.UserListCreate.as_view(), name="user-view-create-account")
]