from django.urls import include, path

from . import views

app_name = "oauth"

urlpatterns = [
    path("google/", include([
        path('redirect', views.google_redirect, name="google_redirect"),
        path('', views.google, name="google")
    ])),
]
