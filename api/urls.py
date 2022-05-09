from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("users/<username>/exists", views.username_exists, name="username_exists"),
]
