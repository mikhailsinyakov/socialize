from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from main.forms import LoginForm


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        context = {"form": form}

        if "google_login_error" in request.session:
            del request.session["google_login_error"]
            context["error_message"] = "An error occured while trying to log in with Google"

        return render(request, "main/login.html", context)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username, password = form.cleaned_data["username"], form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                form = LoginForm(initial={"username": username})
                context = {
                    "error_message": "You have entered an invalid username or password",
                    "form": form
                }
                return render(request, "main/login.html", context)

            login(request, user)
            return HttpResponseRedirect(reverse("main:posts"))
        else:
            context = {"form": form}
            return render(request, "main/login.html", context)


# def login_view(request):
#     if request.method == "GET":
#         context = dict()
#         if "google_login_error" in request.session:
#             del request.session["google_login_error"]
#             context = {
#                 "error_message": "An error occured while trying to log in with Google"
#             }
#         return render(request, "main/login.html", context)
#     elif request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         if not username or not password:
#             context = {
#                 "error_message": "Please fill out all the fields",
#                 "username": username
#             }
#             return render(request, "main/login.html", context)

#         user = authenticate(username=username, password=password)
#         if user is None:
#             context = {
#                 "error_message": "You have entered an invalid username or password",
#                 "username": username
#             }
#             return render(request, "main/login.html", context)

#         login(request, user)
#         return HttpResponseRedirect(reverse("main:posts"))


def signup(request):
    if request.method == "GET":
        return render(request, "main/signup.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if not username:
            context = {
                "error_message": "Please enter an username"
            }
            return render(request, "main/signup.html", context)

        if not password1:
            context = {
                "error_message": "Please enter a password",
                "username": username
            }
            return render(request, "main/signup.html", context)

        if password1 != password2:
            context = {
                "error_message": "Passwords don't match, please retype",
                "username": username
            }
            return render(request, "main/signup.html", context)

        if User.objects.filter(username=username):
            context = {
                "error_message": f"Username '{username}' is already taken",
                "username": username
            }
            return render(request, "main/signup.html", context)

        user = User.objects.create_user(username, None, password1)
        login(request, user)
        return HttpResponseRedirect(reverse("main:posts"))


def add_username(request):
    if request.method == "GET":
        return render(request, "main/add_username.html")
    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        if not username:
            context = {
                "error_message": "Please enter an username"
            }
            return render(request, "main/add_username.html", context)

        if email != request.session["email"]:
            context = {
                "error_message": "You must not change your email",
                "username": username
            }
            return render(request, "main/add_username.html", context)

        if User.objects.filter(username=username):
            context = {
                "error_message": f"Username '{username}' is already taken",
                "username": username
            }
            return render(request, "main/add_username.html", context)

        del request.session["email"]

        user = User.objects.create_user(username, email=email)
        login(request, user)
        return HttpResponseRedirect(reverse("main:posts"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:posts"))


def posts(request):
    return render(request, "main/posts.html")


def index(request):
    return HttpResponseRedirect(reverse("main:posts"))
