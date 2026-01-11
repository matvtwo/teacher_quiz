from django.contrib import admin
from .models import Test, Question
from .ai import generate_questions
import json

@admin.action(description="Generate 50 questions via AI")
def generate_ai_questions(modeladmin, request, queryset):
    for test in queryset:
        raw = generate_questions(test.title)
        data = json.loads(raw)
        for item in data:
            Question.objects.create(
                test=test,
                text=item["question"],
                option_a=item["options"][0],
                option_b=item["options"][1],
                option_c=item["options"][2],
                option_d=item["options"][3],
                correct_answer=item["correct"],
            )

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    actions = [generate_ai_questions]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
