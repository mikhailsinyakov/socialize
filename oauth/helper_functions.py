import requests
from decouple import config
from urllib.parse import urlencode, parse_qs


class ServerError(Exception):
    pass


def get_google_oauth_url():
    google_oauth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    query_params = {
        "client_id": config('GOOGLE_CLIENT_ID'),
        "redirect_uri": config('GOOGLE_REDIRECT_URI'),
        "scope": "https://www.googleapis.com/auth/userinfo.email",
        "response_type": "code",
        "access_type": "offline"
    }
    google_oauth_url = f"{google_oauth_base_url}?{urlencode(query_params)}"

    return google_oauth_url


def get_authorization_code(redirect_url):
    if not "?" in redirect_url:
        redirect_url += "?"
    _, query_string = redirect_url.split("?")
    query_dict = parse_qs(query_string)
    if not "code" in query_dict:
        raise ServerError
    return query_dict["code"]


def get_google_access_token(authorization_code):
    google_oauth_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": authorization_code,
        "client_id": config('GOOGLE_CLIENT_ID'),
        "client_secret": config("GOOGLE_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "redirect_uri": config('GOOGLE_REDIRECT_URI')
    }
    r = requests.post(google_oauth_url, payload,
                      headers={"content-type": "application/x-www-form-urlencoded"})

    if r.status_code != 200:
        raise ServerError
    data = r.json()

    if "access_token" not in data:
        raise ServerError

    return data["access_token"]


def get_email(access_token):
    google_email_api = "https://www.googleapis.com/oauth2/v3/userinfo"
    r = requests.get(google_email_api,
                     headers={"authorization": f"Bearer {access_token}"})

    if r.status_code != 200:
        raise ServerError
    data = r.json()

    if "email" not in data:
        raise ServerError

    return data["email"]


def get_user_email(redirect_url):
    try:
        authorization_code = get_authorization_code(redirect_url)
        access_token = get_google_access_token(authorization_code)
        email = get_email(access_token)

        return email
    except ServerError:
        return None
