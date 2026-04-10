import os
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv
from agents import patient_agent, psychologist_agent, mood_score_agent,supervisor_agent

load_dotenv()
client = OpenAI()

def save_log(text, filename="logs/conversation.txt"):
    os.makedirs("logs", exist_ok=True)
    with open(filename, "a") as f:
        f.write(text + "\n")

def plot_mood(scores):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(scores) + 1), scores, marker="o", linewidth=2, color="steelblue")
    plt.title("Patient Mood Score Across Session")
    plt.xlabel("Turn")
    plt.ylabel("Mood Score (1 = distressed, 10 = calm)")
    plt.ylim(0, 11)
    plt.xticks(range(1, len(scores) + 1))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("logs/mood_chart.png")
    print("\nMood chart saved to logs/mood_chart.png")

def analyze_mood(history):
    conversation_text = "\n".join(
        [f"{'Patient' if m['role'] == 'user' else 'Psychologist'}: {m['content']}"
         for m in history]
    )
    prompt = f"""
You are analyzing a therapy session transcript.
Here is the conversation:
{conversation_text}

Please analyze:
1. The patient's emotional tone at the start vs the end
2. Any shifts in their core belief ("I am bad and worthless")
3. Key turning points in the conversation
4. Overall mood trajectory (e.g. got worse, improved slightly, no change)

Be concise and structured.
"""
    response = client.chat.completions.create(
        model="gpt-5.4-2026-03-05",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_simulation(turns=10):
    history = []
    mood_scores = []

    for i in range(turns):
        print(f"\n{'='*50}")
        print(f"  Turn {i+1}")
        print(f"{'='*50}")
        save_log(f"\n{'='*50}")
        save_log(f"  Turn {i+1}")
        save_log(f"{'='*50}")

        # Patient speaks
        patient_message = patient_agent(history)
        print(f"\nPatient:\n  {patient_message}")
        save_log(f"\nPatient:\n  {patient_message}")
        history.append({"role": "user", "content": patient_message})

        # Score the patient's mood
        score = mood_score_agent(patient_message)
        mood_scores.append(score)
        print(f"\nMood score: {score}/10")
        save_log(f"\nMood score: {score}/10")

        print(f"\n{'-'*50}")
        save_log(f"\n{'-'*50}")

        # Psychologist responds
        psychologist_message = psychologist_agent(history)
        print(f"\nPsychologist:\n  {psychologist_message}")
        save_log(f"\nPsychologist:\n  {psychologist_message}")
        history.append({"role": "assistant", "content": psychologist_message})

        supervisor_feedback = supervisor_agent(patient_message, psychologist_message)
        print(f"\nSupervisor:\n{supervisor_feedback}")
        save_log(f"\nSupervisor:\n{supervisor_feedback}")
        print(f"\n{'='*50}")
        save_log(f"\n{'='*50}")

    # Plot mood chart
    plot_mood(mood_scores)

    # Final analysis
    print(f"\n{'='*50}")
    print("  Mood Analysis")
    print(f"{'='*50}\n")
    analysis = analyze_mood(history)
    print(analysis)
    save_log(f"\n{'='*50}")
    save_log("  Mood Analysis")
    save_log(f"{'='*50}\n")
    save_log(analysis)