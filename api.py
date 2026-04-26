from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from simulation import analyze_mood
import json
import re
import asyncio
from agents import patient_agent, psychologist_agent, mood_score_agent, supervisor_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Patient-Ψ API",
    description="Role-play with an AI patient or psychologist based on the Patient-Ψ framework.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    history: list
    message: str

def clean_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # remove **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)        # remove *italic*
    text = re.sub(r'#{1,6}\s', '', text)             # remove headers
    text = text.strip()
    return text

@app.get("/")
def root():
    return {
        "name": "Patient-Ψ API",
        "endpoints": {
            "POST /talk-to-patient": "You play the psychologist, AI plays the patient",
            "POST /talk-to-psychologist": "You play the patient, AI plays the psychologist",
            "GET /simulate": "Watch the 3 agents simulate a full session"
        }
    }

@app.post("/talk-to-patient")
def talk_to_patient(body: Message):
    history = body.history
    history.append({"role": "assistant", "content": body.message})
    response = clean_text(patient_agent(history))
    history.append({"role": "user", "content": response})
    return {"response": response, "history": history}

@app.post("/talk-to-psychologist")
def talk_to_psychologist(body: Message):
    history = body.history
    history.append({"role": "user", "content": body.message})
    response = clean_text(psychologist_agent(history))
    history.append({"role": "assistant", "content": response})
    return {"response": response, "history": history}

@app.get("/simulate")
async def simulate(turns: int = 10):
    async def event_stream():
        history = []

        for i in range(turns):
            yield f"data: {json.dumps({'type': 'turn', 'turn': i + 1})}\n\n"
            await asyncio.sleep(0.3)

            # Patient speaks
            patient_message = clean_text(patient_agent(history))
            history.append({"role": "user", "content": patient_message})
            yield f"data: {json.dumps({'type': 'patient', 'content': patient_message})}\n\n"
            await asyncio.sleep(0.3)

            # Mood score
            score = mood_score_agent(patient_message)
            yield f"data: {json.dumps({'type': 'mood', 'score': score})}\n\n"
            await asyncio.sleep(0.3)

            # Psychologist responds
            psychologist_message = clean_text(psychologist_agent(history))
            history.append({"role": "assistant", "content": psychologist_message})
            yield f"data: {json.dumps({'type': 'psychologist', 'content': psychologist_message})}\n\n"
            await asyncio.sleep(0.3)

            # Supervisor feedback
            feedback = clean_text(supervisor_agent(patient_message, psychologist_message))
            yield f"data: {json.dumps({'type': 'supervisor', 'content': feedback})}\n\n"
            await asyncio.sleep(0.5)

        # Final analysis
        analysis = clean_text(analyze_mood(history))
        yield f"data: {json.dumps({'type': 'analysis', 'content': analysis})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )