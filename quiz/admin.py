from django.contrib import admin
from .models import Test, Question, Attempt

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "text", "correct")
    list_filter = ("test",)
    search_fields = ("text",)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname", "test", "score", "total", "created_at")
    list_filter = ("test", "created_at")
    search_fields = ("nickname",)
    ordering = ("-created_at",)
