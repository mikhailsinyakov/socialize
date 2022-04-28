from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("posts/", views.posts, name="posts"),
    path("", views.index, name="index"),
]
