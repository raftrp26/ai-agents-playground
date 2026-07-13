import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def transcribe_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio,
        )

    return transcript.text