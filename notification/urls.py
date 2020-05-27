from django.urls import path
from .views import view_notifications

urlpatterns = [
    path("notifications/", view_notifications)
]