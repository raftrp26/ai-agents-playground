import os
import tempfile
from fastapi import FastAPI, UploadFile 
from transcriptAudio import transcribe_audio
from event_interpreter import interpret_calendar_event
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Secretary AI API is running!"}

@app.post("/execute")
async def execute(audio: UploadFile):
    extension = os.path.splitext(audio.filename or "")[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temporary_file:
        content = await audio.read()
        temporary_file.write(content)
        temporary_path = temporary_file.name

    try:
        transcription = transcribe_audio(temporary_path)
        now = datetime.now(ZoneInfo("Europe/Lisbon"))
        event_call = interpret_calendar_event(transcription, now)

        return {
            "status": "interpreted",
            "transcription": transcription,
            "event": event_call.model_dump(mode="json")
        }
    finally:
        os.remove(temporary_path)