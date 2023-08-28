from django.db import models

class MonthlyNewVisitors(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    new_visitors_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'month')  # 동일한 연도와 월에 대한 데이터는 중복으로 저장되지 않게 설정
