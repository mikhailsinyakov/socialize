from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from main.models import Profile
from django.core.mail import send_mail

from random import randint

def username_exists(request, username):
    if request.method == "GET":
        exists = bool(User.objects.filter(username=username))
        return JsonResponse({"username_exists": exists})
    else:
        return HttpResponseNotAllowed(["GET"])


def send_email(request, username):
    if request.method == "POST":
        email = User.objects.get(username=username).email
        verification_code = randint(100000, 999999)
        send_mail(
            "Socialize",
            f"Your verification code is {verification_code}",
            None,
            [email],
            fail_silently=False,
        )
        return JsonResponse({"verification_code": verification_code})
    else:
        return HttpResponseNotAllowed(["POST"])


def verify_email(request, username):
    if request.method == "POST":
        profile = Profile.objects.get(user__username=username)
        profile.is_email_verified = True
        profile.save()
        return HttpResponse("")
    else:
        return HttpResponseNotAllowed(["POST"])