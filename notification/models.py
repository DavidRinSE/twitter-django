from django.db import models
from twitteruser.models import TwitteruserModel
from tweet.models import TweetModel
# Create your models here.


class NotificationModel(models.Model):
    user = models.ForeignKey(TwitteruserModel, on_delete=models.CASCADE)
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)