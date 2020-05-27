from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import re
from .forms import TweetForm
from .models import TweetModel
from twitteruser.views import GET_INFO
from notification.models import NotificationModel
from twitteruser.models import TwitteruserModel
# Create your views here.


@login_required
def create_tweet(request):
    html = "tweet.html"

    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            tweet = TweetModel.objects.create(
                text=data["text"],
                postedBy=request.user
            )
            
            tag = re.search(r'(?<=@)\w+', data['text'])
            if tag and tag.group(0):
                try:
                    user = TwitteruserModel.objects.get(username=tag.group(0))
                    NotificationModel.objects.create(
                        user=user,
                        tweet=tweet
                    )
                except TweetuserModel.DoesNotExist:
                    pass
            if tweet:
                return HttpResponseRedirect(reverse("homepage"))

    info = GET_INFO(request, request.user)
    form = TweetForm()
    return render(request, html, {
        "form": form,
        "username": request.user.username,
        "tweetcount": len(info['tweets']),
        "followingcount": len(info['following']),
        "action": info["action"],
        "toggle": info["toggle"],
    })


def view_tweet(request, id):
    html = "view_tweet.html"

    try:
        tweet = TweetModel.objects.get(id=id)
    except TweetModel.DoesNotExist:
        print("Bang")
        return HttpResponseRedirect("/")

    info = GET_INFO(tweet.postedBy)
    return render(request, html, {
        "username": tweet.postedBy.username,
        "tweetcount": len(info["tweets"]),
        "followingcount": len(info["following"]),
        "tweet":tweet,
        "action": info["action"],
        "toggle": info["toggle"],
    })