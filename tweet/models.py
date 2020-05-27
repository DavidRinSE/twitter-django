from django.db import models
from django.utils import timezone
from twitteruser.models import TwitteruserModel
# Create your models here.


class TweetModel(models.Model):
    text = models.CharField(max_length=140)
    dateFiled = models.DateTimeField(default=timezone.now)
    postedBy = models.ForeignKey(TwitteruserModel, on_delete=models.CASCADE)