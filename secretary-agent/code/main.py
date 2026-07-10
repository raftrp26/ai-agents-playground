# Testing OpenAIKey
# import os
# from dotenv import load_dotenv

# load_dotenv()

# print(os.getenv("OPENAI_API_KEY"))

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

with open("audio/Audio1Teste.mp4", "rb") as audio:
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=audio,
    )

print(transcript.text)