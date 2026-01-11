import os
import requests

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

def generate_questions(topic, count=50):
    prompt = f"""
Сгенерируй {count} тестовых вопросов по теме "{topic}".
Формат строго JSON:
[
  {{
    "question": "Текст вопроса",
    "options": ["A", "B", "C", "D"],
    "correct": 0
  }}
]
"""
    response = requests.post(
        DEEPSEEK_URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
