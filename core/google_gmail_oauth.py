from google_auth_oauthlib.flow import Flow
from django.conf import settings

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def build_google_flow():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_GMAIL_CLIENT_ID,
                "client_secret": settings.GOOGLE_GMAIL_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_GMAIL_REDIRECT_URI],
            }
        },
        scopes=GMAIL_SCOPES,
    )
    flow.redirect_uri = settings.GOOGLE_GMAIL_REDIRECT_URI
    return flow