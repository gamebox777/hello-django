from django.db import models

class Record(models.Model):
    name = models.CharField(max_length=30)
    win_streak = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.win_streak}連勝 ({self.played_at:%Y-%m-%d %H:%M})" 