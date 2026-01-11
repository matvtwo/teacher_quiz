from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Attempt

def home(request):
    if request.method == "POST":
        nickname = (request.POST.get("nickname") or "").strip()
        if nickname:
            request.session["nickname"] = nickname
            return redirect("tests")
    return render(request, "quiz/home.html", {"nickname": request.session.get("nickname", "")})


def tests(request):
    all_tests = Test.objects.order_by("-id")
    return render(request, "quiz/tests.html", {"tests": all_tests, "nickname": request.session.get("nickname")})


def take_test(request, test_id: int):
    nickname = request.session.get("nickname")
    if not nickname:
        return redirect("home")

    test = get_object_or_404(Test, id=test_id)
    questions = list(test.questions.order_by("id"))
    total = len(questions)

    if request.method == "POST":
        score = 0
        for q in questions:
            picked = request.POST.get(f"q_{q.id}")
            if picked and picked.isdigit() and int(picked) == q.correct:
                score += 1

        Attempt.objects.create(
            nickname=nickname,
            test=test,
            score=score,
            total=total,
        )
        return render(request, "quiz/result.html", {
            "test": test,
            "nickname": nickname,
            "score": score,
            "total": total
        })

    return render(request, "quiz/take_test.html", {
        "test": test,
        "nickname": nickname,
        "questions": questions
    })
