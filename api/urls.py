from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("users/<username>/exists", views.username_exists, name="username_exists"),
    path("users/<username>/send_email", views.send_email, name="send_email"),
    path("users/<username>/verify_email", views.verify_email, name="verify_email"),
]
