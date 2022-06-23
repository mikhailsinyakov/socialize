from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        min_length=6, widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data:
            raise ValidationError(
                "Please enter an username", code='no_username')
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        if not data:
            raise ValidationError(
                "Please enter a password", code='no_password')
        return data


class SignupForm(forms.Form):
    username = forms.CharField(
        min_length=3, widget=forms.TextInput(attrs={'autofocus': True}))
    password1 = forms.CharField(
        min_length=6, label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        min_length=6, label="Confirm Password", widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data:
            raise ValidationError(
                "Please enter an username", code='no_username')
        if len(data) < 3:
            raise ValidationError(
                "Username should be at least 3 characters", code='short_username')
        return data

    def clean_password1(self):
        data = self.cleaned_data["password1"]
        if not data:
            raise ValidationError(
                "Please enter a password", code='no_password')
        if len(data) < 6:
            raise ValidationError(
                "Password should be at least 6 characters", code='short_password')
        return data

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", ValidationError(
                    "Passwords don't match, please retype", code='passwords_dont_match'))


class AddUsernameForm(forms.Form):
    username = forms.CharField(
        min_length=3, widget=forms.TextInput(attrs={'autofocus': True}))
    email = forms.EmailField(disabled=True)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data:
            raise ValidationError(
                "Please enter an username", code='no_username')
        if len(data) < 3:
            raise ValidationError(
                "Username should be at least 3 characters", code='short_username')
        return data
