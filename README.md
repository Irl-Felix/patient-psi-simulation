# Patient-Ψ Simulation — AI Therapy Agent System

A multi-agent simulation of a cognitive behavioral therapy (CBT) session, 
inspired by the Patient-Ψ research paper. Three AI agents (a patient, a 
psychologist, and a clinical supervisor) conduct and evaluate a full therapy 
session autonomously, with mood tracking and analysis.

---

## Overview

This project simulates a therapy session between three GPT-powered agents:

- **Patient Agent** — built on a full cognitive model (core beliefs, automatic 
  thoughts, emotions, behaviors) derived from the Patient-Ψ paper
- **Psychologist Agent** — conducts CBT-style therapy using Socratic questioning 
  and guided discovery
- **Supervisor Agent** — observes each exchange and provides clinical feedback 
  on the psychologist's technique after every turn
- **Mood Scorer** — rates the patient's emotional state after each turn (1–10)
- **Analyzer** — generates a structured analysis of the full session at the end

---

## Project Structure

```
patient_simulation/
├── main.py           # Entry point
├── agents.py         # Agent functions (patient, psychologist, supervisor, mood scorer)
├── prompts.py        # Cognitive model prompts for each agent
├── simulation.py     # Conversation loop, logging, mood chart, analysis
├── logs/             # Saved conversation transcripts and mood chart
├── .env              # Your OpenAI API key (not committed to git)
└── pyproject.toml    # Dependencies managed by uv
```

---

## Cognitive Model (Patient-Ψ)

The patient is built using 8 components from the Patient-Ψ framework:

**Foundational (long-term psychological makeup)**
- Relevant History
- Core Beliefs
- Intermediate Beliefs
- Coping Strategies

**Situational (session trigger)**
- Situation
- Automatic Thoughts
- Emotions
- Behaviors

---

## How It Works

Each turn follows this sequence:

1. 🧑 Patient speaks based on their cognitive profile and conversation history
2. 📈 Mood scorer rates the patient's emotional state (1–10)
3. 🧠 Psychologist responds using CBT techniques
4. 👁️  Supervisor evaluates the psychologist's response and suggests improvements
5. Repeat for N turns
6. 📊 Mood chart generated from all scores
7. 📝 Final written analysis of the full session

---

## Supervisor Agent

The supervisor observes every exchange and provides structured clinical feedback after each turn:

| | Feedback |
|---|---|
| ✅ | What the psychologist did well |
| ⚠️ | What could be improved |
| 💡 | Suggested technique for the next turn |

**Evaluation criteria:**
- Use of open-ended questions
- Empathy and validation
- Socratic questioning
- Avoiding premature advice
- Catching emotional cues from the patient

---

## Mood Scoring

The mood scorer rates each patient message on a scale of 1–10:

| Score | Interpretation |
|-------|----------------|
| 1–3   | Distressed, hopeless, deeply negative |
| 4–6   | Mixed, neutral, some openness |
| 7–10  | Calm, hopeful, belief shifts emerging |

This allows quantitative comparison across sessions, profiles, and techniques.

---

## Setup

**1. Install uv**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Clone and install dependencies**
```bash
git clone https://github.com/Irl-Felix/patient-psi-simulation.git
cd patient-psi-simulation
uv sync
```

**3. Add your OpenAI API key**

Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

**4. Run the simulation**
```bash
uv run python main.py
```

---

## Output

Each run produces:

- A live conversation printed to the terminal, turn by turn
- A mood score (1–10) after each patient message
- Clinical supervisor feedback after each psychologist response
- A saved transcript at logs/conversation.txt
- A mood trajectory chart at logs/mood_chart.png
- A written analysis of belief shifts and emotional arc

---

## Models Used

| Agent          | Model                    |
|----------------|--------------------------|
| Patient        | gpt-5.4-mini-2026-03-17  |
| Psychologist   | gpt-5.4-mini-2026-03-17  |
| Supervisor     | gpt-5.4-2026-03-05       |
| Mood Scorer    | gpt-5.4-2026-03-05       |
| Analyzer       | gpt-5.4-2026-03-05       |

---

## Research Reference

Inspired by:
> Patient-Ψ: Using Large Language Models to Simulate Patients for Training 
> Mental Health Professionals

---

## Future Work

- Multiple patient profiles (depression, trauma, anger)
- Multi-session memory to track long-term progress
- JSON logging for structured data analysis
- Supervisor score for psychologist performance over time
- Automated comparison across CBT techniques