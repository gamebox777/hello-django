from django.db import models

# Create your models here.

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('EATING', '食習慣'),
        ('BODY', '健康・老化'),
        ('MIND', '性格・ストレス'),
        ('ECOLOGY', '環境汚染'),
        ('SURVIVAL', 'サバイバル'),
        ('WILD', 'ワイルドカード'),
    ]
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    text = models.CharField(max_length=255)
    correct_yes = models.BooleanField()

    def __str__(self):
        return f"[{self.category}] {self.text}"

class QuizSession(models.Model):
    user_id = models.CharField(max_length=64)  # セッションIDやIP等
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    lp_total = models.IntegerField(default=0)

class Answer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_choice = models.CharField(max_length=3)  # 'Yes' or 'No'
    is_correct = models.BooleanField()

class Result(models.Model):
    session = models.OneToOneField(QuizSession, on_delete=models.CASCADE)
    lifespan_years = models.IntegerField()
    xday_date = models.DateField()
