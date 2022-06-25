from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField()
    error = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.user.username
