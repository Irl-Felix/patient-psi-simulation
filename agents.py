import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PATIENT_PROMPT, PSYCHOLOGIST_PROMPT, SUPERVISOR_PROMPT

load_dotenv()
client = OpenAI()

def patient_agent(history):
    messages = [{"role": "system", "content": PATIENT_PROMPT}]
    messages += history
    response = client.chat.completions.create(
        model="gpt-5.4-mini-2026-03-17",
        messages=messages
    )
    return response.choices[0].message.content

def psychologist_agent(history):
    messages = [{"role": "system", "content": PSYCHOLOGIST_PROMPT}]
    messages += history
    response = client.chat.completions.create(
        model="gpt-5.4-mini-2026-03-17",
        messages=messages
    )
    return response.choices[0].message.content

def mood_score_agent(patient_message):
    prompt = f"""
Rate the emotional state of this patient message on a scale from 1 to 10.
1 = extremely distressed, hopeless, negative
10 = calm, positive, hopeful

Patient message:
\"{patient_message}\"

Reply with a single integer between 1 and 10. Nothing else.
"""
    response = client.chat.completions.create(
        model="gpt-5.4-2026-03-05",
        messages=[{"role": "user", "content": prompt}]
    )
    score = response.choices[0].message.content.strip()
    return int(score)

def supervisor_agent(patient_message, psychologist_message):
    prompt = f"""
Patient said:
\"{patient_message}\"

Psychologist responded:
\"{psychologist_message}\"

Provide your clinical supervision feedback.
"""
    messages = [
        {"role": "system", "content": SUPERVISOR_PROMPT},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-5.4-2026-03-05",
        messages=messages
    )
    return response.choices[0].message.content