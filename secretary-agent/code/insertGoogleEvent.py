# event = {
#     "summary": "Primeiro teste da API",

#     "start": {
#         "dateTime": "2026-07-11T19:00:00",
#         "timeZone": "Europe/Lisbon"
#     },

#     "end": {
#         "dateTime": "2026-07-11T20:00:00",
#         "timeZone": "Europe/Lisbon"
#     }
# }


# Autenticação
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]

CREDENTIALS_PATH = "credentials/googleOauthClient.json"
TOKEN_PATH = "credentials/token.json"

def get_calendar_service():

    credentials = None

    if os.path.exists(TOKEN_PATH):
        print("📁 Token encontrado.")
        credentials = Credentials.from_authorized_user_file(
            TOKEN_PATH,
            SCOPES,
        )
    else:
        print("📁 Nenhum token encontrado.")
    if not credentials or not credentials.valid:
        print("⚠️ Credenciais inválidas.")

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            print("🔄 Renovando token automaticamente...")
            credentials.refresh(Request())

        else:
            print("🌐 Iniciando autenticação OAuth...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES,
            )

            credentials = flow.run_local_server(
                port=0,
                open_browser=False,
            )

        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(credentials.to_json())

    else:
        print("✅ Token válido. Login não é necessário.")


    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )

print("Autenticação realizada com sucesso!")
#print(credentials.valid)
print("Serviço do Google Calendar criado com sucesso!")


# Creating google calendar event

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def create_calendar_event(service, event):
    event_body = {
        "summary": event.title,
        "start": {
            "dateTime": event.start_datetime,
            "timeZone": event.timezone,
        },
        "end": {
            "dateTime": event.end_datetime,
            "timeZone": event.timezone,
        },
    }

    if event.description:
        event_body["description"] = event.description

    if event.location:
        event_body["location"] = event.location

    if event.attendees:
        event_body["attendees"] = [
            {"email": email}
            for email in event.attendees
        ]

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event_body,
            sendUpdates="all" if event.attendees else "none",
        )
        .execute()
    )

    print("\n✅ Evento criado com sucesso!")
    print(f"Título: {created_event.get('summary')}")
    print(f"ID: {created_event.get('id')}")
    print(f"Link: {created_event.get('htmlLink')}")

    return created_event