from django.urls import path
from tweet import views
urlpatterns = [
    path("tweet/", views.create_tweet),
    path("tweet/<int:id>/", views.view_tweet)
]