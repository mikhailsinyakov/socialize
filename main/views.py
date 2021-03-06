from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from main.forms import LoginForm, SignupForm, AddUsernameForm
from main.models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main:posts"))
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
        
        context = {"form": form}
        return render(request, "main/login.html", context)

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main:posts"))
    if request.method == "GET":
        form = SignupForm()
        context = {"form": form}
        return render(request, "main/signup.html", context)
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username, email = form.cleaned_data["username"], form.cleaned_data["email"]
            password1, password2 = form.cleaned_data["password1"], form.cleaned_data["password2"]
            if email == "": email = None
            if User.objects.filter(username=username):
                form = SignupForm()
                context = {
                    "error_message": f"Username '{username}' is already taken",
                    "form": form
                }
                return render(request, "main/signup.html", context)
            if email and User.objects.filter(email=email):
                current_profile = Profile.objects.get(user__email=email)
                
                context = {"form": SignupForm()}
                if current_profile.is_email_verified:
                    context["error_message"] = f"Email '{email}' is already taken"
                else:
                    context["error_message"] = f"Email '{email}' is used by another user. If it is your email, you can sign up via Google"
                return render(request, "main/signup.html", context)

            user = User.objects.create_user(username, email, password1)
            profile = Profile.objects.create(user=user, is_email_verified=False)
            login(request, user)
            if email is None:
                return HttpResponseRedirect(reverse("main:posts"))
            return HttpResponseRedirect(reverse("main:confirm_email"))
        
        context = {"form": form}
        return render(request, "main/signup.html", context)
    
def add_username(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main:posts"))
    if request.method == "GET":
        form = AddUsernameForm(initial={"email": request.session["email"]})
        context = {"form": form}
        return render(request, "main/add_username.html", context)
    elif request.method == "POST":
        form = AddUsernameForm(request.POST, initial={"email": request.session["email"]})
        if form.is_valid():
            username, email = form.cleaned_data["username"], request.session["email"]
            if User.objects.filter(username=username):
                form = AddUsernameForm(initial={"email": email})
                context = {
                    "error_message": f"Username '{username}' is already taken",
                    "form": form
                }
                return render(request, "main/add_username.html", context)
            del request.session["email"]

            user = User.objects.create_user(username, email=email)
            profile = Profile.objects.create(user=user, is_email_verified=True)
            login(request, user)
            return HttpResponseRedirect(reverse("main:posts"))

        context = {"form": form}
        return render(request, "main/signup.html", context)

def confirm_email(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            profile = Profile.objects.get(user__username=request.user.username)
            if not profile.is_email_verified:
                context = {"email": request.user.email, "username": request.user.username}
                return render(request, "main/confirm_email.html", context)

    return HttpResponseRedirect(reverse("main:posts"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main:posts"))


def posts(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user__username=request.user.username)
        if profile.error:
            context["error"] = profile.error
            profile.error = ""
            profile.save()
    return render(request, "main/posts.html", context)


def index(request):
    return HttpResponseRedirect(reverse("main:posts"))
