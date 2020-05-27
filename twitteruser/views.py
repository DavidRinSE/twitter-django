from .forms import CreateUserForm
from .models import TwitteruserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, reverse, HttpResponseRedirect

from tweet.models import TweetModel
from .models import TwitteruserModel
# Create your views here.
@login_required
def index(request, profile=None):
    if profile:
        try:
            user = TwitteruserModel.objects.get(username=profile)
        except TwitteruserModel.DoesNotExist:
            return HttpResponseRedirect("/")
    else:
        user = request.user

    info = GET_INFO(request, user)

    tweets = info["tweets"]

    if not profile:
        for follow in info['following']:
            try:
                tweets = tweets | TweetModel.objects.all().filter(postedBy=follow)
            except TweetModel.DoesNotExist:
                pass

    return render(request, "index.html", 
        {
            "username": user.username,
            "tweetcount": len(info['tweets']),
            "followingcount": len(info['following']),
            "action": info['action'],
            "toggle": info["toggle"],
            "tweets": tweets.order_by('-dateFiled')
        })


def create_user(request):
    html = "createuserform.html"

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = TwitteruserModel.objects.create(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )

    form = CreateUserForm()
    return render(request, html, {"form": form})


@login_required
def toggle_follow(request, username):

    try:
        user = TwitteruserModel.objects.get(username=username)
    except TwitteruserModel.DoesNotExist:
        HttpResponseRedirect("/")

    if user in request.user.following.all():
        request.user.following.remove(user)
    else:
        request.user.following.add(user)
        request.user.save()

    return HttpResponseRedirect("/")


def GET_INFO(request, user):
    following = user.following.all()

    try:
        tweets = TweetModel.objects.all().filter(postedBy=user)
    except TweetModel.DoesNotExist:
        tweets = None

    action = None
    if request.user != user:
        if user not in request.user.following.all():
            action = "Follow"
        else:
            action = "Unfollow"

    return{
        "following": following,
        "tweets": tweets,
        "action": action,
        "toggle": reverse("toggle", kwargs={"username":user.username}),
    }