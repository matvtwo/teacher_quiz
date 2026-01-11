import os, json, requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"

@csrf_exempt
def generate_question(request):
    topic = request.GET.get("topic", "Общая тема")
    prompt = f"""
Сгенерируй ОДИН тестовый вопрос по теме "{topic}".
Формат строго JSON:
{{
  "question": "...",
  "options": ["A","B","C","D"],
  "correct": 0
}}
"""
    r = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
        timeout=20,
    )
    data = json.loads(r.json()["choices"][0]["message"]["content"])
    return JsonResponse(data)
