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

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]

CREDENTIALS_PATH = "credentials/googleOauthClient.json"


flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_PATH,
    SCOPES,
)

credentials = flow.run_local_server(
    port=0,
    open_browser=False,
)

print("Autenticação realizada com sucesso!")
print(credentials.valid)

service = build(
    "calendar",
    "v3",
    credentials=credentials,
)

print("Serviço do Google Calendar criado com sucesso!")