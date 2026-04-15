from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents import patient_agent, psychologist_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Patient-Ψ API",
    description="Role-play with an AI patient or psychologist based on the Patient-Ψ framework.",
    version="1.0.0"
)

# Add this block
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

@app.get("/")
def root():
    return {
        "name": "Patient-Ψ API",
        "endpoints": {
            "POST /talk-to-patient": "You play the psychologist, AI plays the patient",
            "POST /talk-to-psychologist": "You play the patient, AI plays the psychologist"
        }
    }

@app.post("/talk-to-patient")
def talk_to_patient(body: Message):
    history = body.history
    history.append({"role": "assistant", "content": body.message})
    response = patient_agent(history)
    history.append({"role": "user", "content": response})
    return {"response": response, "history": history}

@app.post("/talk-to-psychologist")
def talk_to_psychologist(body: Message):
    history = body.history
    history.append({"role": "user", "content": body.message})
    response = psychologist_agent(history)
    history.append({"role": "assistant", "content": response})
    return {"response": response, "history": history}