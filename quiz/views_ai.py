import json
import threading
import time
import os
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Test

API_KEY = os.environ["DEEPSEEK_API_KEY"]
BASE_URL = os.environ["DEEPSEEK_BASE_URL"]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SYSTEM_PROMPT = """
Сгенерируй ОДИН тестовый вопрос.

Формат строго:

QUESTION:
<текст>

OPTIONS:
1) ...
2) ...
3) ...
4) ...

ANSWER:
<номер правильного варианта>
"""

def ask_ai(user_prompt: str) -> str:
    r = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def worker(test_id: int, prompt: str, count: int):
    test = Test.objects.get(id=test_id)

    for _ in range(count):
        try:
            raw = ask_ai(prompt)

            q_part, rest = raw.split("OPTIONS:")
            opts_part, ans_part = rest.split("ANSWER:")

            options = opts_part.strip().splitlines()

            Question.objects.create(
                test=test,
                text=q_part.replace("QUESTION:", "").strip(),
                option_1=options[1][3:].strip(),
                option_2=options[2][3:].strip(),
                option_3=options[3][3:].strip(),
                option_4=options[4][3:].strip(),
                correct=int(ans_part.strip()),
            )

            time.sleep(1)
        except Exception as e:
            print("AI ERROR:", e)


@csrf_exempt
def generate_questions_async(request):
    data = json.loads(request.body)
    prompt = data.get("prompt", "").strip()
    count = int(data.get("count", 5))

    test = Test.objects.last()
    if not test:
        return JsonResponse({"error": "Нет теста"}, status=400)

    threading.Thread(
        target=worker,
        args=(test.id, prompt, count),
        daemon=True,
    ).start()

    return JsonResponse({"status": "started"})
