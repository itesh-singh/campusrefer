import base64
from email.mime.text import MIMEText

from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


GMAIL_SCOPE = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_credentials():
    creds = Credentials(
        token=None,
        refresh_token=settings.GOOGLE_GMAIL_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_GMAIL_CLIENT_ID,
        client_secret=settings.GOOGLE_GMAIL_CLIENT_SECRET,
        scopes=GMAIL_SCOPE,
    )
    creds.refresh(Request())
    return creds


def send_gmail_message(to_email: str, subject: str, body: str):
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    message = MIMEText(body, "html")
    message["to"] = to_email
    message["from"] = settings.GOOGLE_GMAIL_SENDER
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    payload = {"raw": raw_message}

    return service.users().messages().send(userId="me", body=payload).execute()