from django.urls import path
from twitteruser import views


urlpatterns = [
    path("", views.index, name="homepage"),
    path("createuser/", views.create_user),
    path("togglefollow/<str:username>/", views.toggle_follow, name="toggle"),
    path("<str:profile>/", views.index, name="profile"),
]