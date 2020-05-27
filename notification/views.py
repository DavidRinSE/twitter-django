from django.shortcuts import render
from .models import NotificationModel
from twitteruser.views import GET_INFO
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def view_notifications(request):
    user = request.user
    info = GET_INFO(request, user)
    notifications = NotificationModel.objects.all().filter(user=user)
    for notification in notifications:
        NotificationModel.delete(notification)
    return render(request, "notifications.html",
        {
            "username":user.username,
            "tweetcount": len(info["tweets"]),
            "followingcount": len(info['following']),
            "notifications": notifications,
            "action": info["action"],
            "toggle": info["toggle"],
        })