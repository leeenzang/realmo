from django.db import models

class DailyNewVisitors(models.Model):
    date = models.DateField(unique=True)
    new_visitors_count = models.PositiveIntegerField()

class MonthlyNewVisitors(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    new_visitors_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'month')
