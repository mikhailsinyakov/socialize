from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse


def login_view(request):
    if request.method == "GET":
        return render(request, "main/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            context = {
                "error_message": "Please fill out all the fields",
                "username": username
            }
            return render(request, "main/login.html", context)

        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                "error_message": "You have entered an invalid username or password",
                "username": username
            }
            return render(request, "main/login.html", context)

        login(request, user)
        return HttpResponseRedirect(reverse("main:posts"))


def posts(request):
    username = request.user.username if request.user.is_authenticated else "guest"
    return render(request, "main/posts.html", {"username": username})


def index(request):
    return HttpResponseRedirect(reverse("main:posts"))
