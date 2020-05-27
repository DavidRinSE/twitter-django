from .forms import LoginForm
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_view(request):
    html = "loginform.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )

    form = LoginForm()
    return render(request, html, {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))