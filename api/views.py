from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User


def username_exists(request, username):
    if request.method == "GET":
        exists = bool(User.objects.filter(username=username))
        return JsonResponse({"username_exists": exists})
    else:
        return HttpResponseNotAllowed(["GET"])
