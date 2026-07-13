# Testing OpenAIKey
# import os
# from dotenv import load_dotenv

# load_dotenv()

# print(os.getenv("OPENAI_API_KEY"))

# import os

# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# with open("audio/Audio1Teste.mp4", "rb") as audio:
#     transcript = client.audio.transcriptions.create(
#         model="gpt-4o-transcribe",
#         file=audio,
#     )

# print(transcript.text)

from datetime import datetime
from zoneinfo import ZoneInfo

from event_interpreter import interpret_calendar_event
from transcriptAudio import transcribe_audio
from insertGoogleEvent import create_calendar_event, get_calendar_service


now = datetime.now(ZoneInfo("Europe/Lisbon"))

# Input audio

audio_path = "audio/Audio1Teste.mp4"
conversation = transcribe_audio(audio_path)


while True:
    event = interpret_calendar_event(
        transcription=conversation,
        current_datetime=now,
    )

    if event.status == "needs_clarification":
        print("\nPreciso de mais algumas informações:")

        answers = []

        for question in event.clarification_questions:
            answer = input(f"- {question}\n> ").strip()

            answers.append(
                f"Pergunta: {question}\n"
                f"Resposta do usuário: {answer}"
            )

        conversation += (
            "\n\nInformações adicionais fornecidas pelo usuário:\n"
            + "\n".join(answers)
        )

        continue

    break

print("\nEvento interpretado:")
print(f"Título: {event.title}")
print(f"Início: {event.start_datetime}")
print(f"Fim: {event.end_datetime}")
print(f"Fuso: {event.timezone}")
print(f"Local: {event.location or 'Não informado'}")
print(f"Descrição: {event.description or 'Não informada'}")

confirmation = input(
    "\nOs dados estão corretos? Deseja criar o evento? [s/n]: "
).strip().lower()

service = get_calendar_service()

if confirmation in ["s", "sim"]:
    create_calendar_event(
        service=service,
        event=event,
    )
else:
    print("Criação do evento cancelada.")