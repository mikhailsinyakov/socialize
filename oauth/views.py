from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Profile

from oauth.helper_functions import get_google_oauth_url, get_user_email


def google(request):
    return HttpResponseRedirect(get_google_oauth_url())


def google_redirect(request):
    # if user typed the redirect url in a browser
    if request.headers.get("Sec-Fetch-Site") == "none":
        return HttpResponseRedirect(reverse("main:login"))

    redirect_url = request.get_full_path()
    email = get_user_email(redirect_url)

    if email is None:
        request.session["google_login_error"] = True
        return HttpResponseRedirect(reverse("main:login"))

    users = User.objects.filter(email=email)
    if users:
        user = users[0]
        profile = Profile.objects.get(user__email=email)
        if profile.is_email_verified:
            login(request, user)
            return HttpResponseRedirect(reverse("main:posts"))
        
        profile.error = "Your email has been deleted because another user used it when signing up via Google"
        profile.save()
        user.email = ""
        user.save()

    request.session["email"] = email
    return HttpResponseRedirect(reverse("main:add_username"))
