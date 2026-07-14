import os
import tempfile
from fastapi import FastAPI, UploadFile 
from transcriptAudio import transcribe_audio
from event_interpreter import interpret_calendar_event
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel

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

        if event_call.status == "needs_clarification":
            return {
                "status": "needs_clarification",
                "questions": event_call.clarification_questions,
                "event": event_call.model_dump(mode="json")
            }
        if event_call.status == "ready_for_confirmation":
            return {
                "status": "ready_for_confirmation",
                "event": event_call.model_dump(mode="json")
            }
    finally:
        os.remove(temporary_path)

class ClarificationRequest(BaseModel):
    answer: str

@app.post("/clarify")
def clarify(request: ClarificationRequest):
    return {
        "received_answer": request.answer
    }