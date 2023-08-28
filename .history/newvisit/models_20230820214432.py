from django.db import models


# 일별 신규 방문자 수 저장
class DailyNewVisitors(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.count} 신규 방문자"

# 월별 신규 방문자 수 저장
class MonthlyNewVisitors(models.Model):
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('year', 'month')

    def __str__(self):
        return f"{self.year}-{self.month} - {self.count} 신규 방문자"
