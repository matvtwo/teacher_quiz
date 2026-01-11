from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)

    # 1..4
    correct = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.test.title}: {self.text[:40]}"


class Attempt(models.Model):
    nickname = models.CharField(max_length=100)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nickname} — {self.score}/{self.total} — {self.test.title}"
