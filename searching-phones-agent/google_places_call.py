import os

import requests
from dotenv import load_dotenv


load_dotenv("../.env")

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
GOOGLE_PLACES_URL = "https://places.googleapis.com/v1/places:searchText"


def call_places_in_google(text_query):
    if not GOOGLE_PLACES_API_KEY:
        raise RuntimeError("GOOGLE_PLACES_API_KEY não encontrada no .env.")

    google_headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.id,"
            "places.displayName,"
            "places.formattedAddress,"
            "places.internationalPhoneNumber"
        ),
    }

    google_body = {
        "textQuery": text_query,
        "languageCode": "pt-PT",
        "pageSize": 5,
    }

    response = requests.post(
        GOOGLE_PLACES_URL,
        headers=google_headers,
        json=google_body,
        timeout=30,
    )

    if not response.ok:
        print(response.status_code)
        print(response.text)

    response.raise_for_status()

    return response.json().get("places", [])