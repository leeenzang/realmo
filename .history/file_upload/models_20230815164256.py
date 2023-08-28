from django.db import models

class Visitor(models.Model):
    UID = models.CharField(max_length=200)
    사용일 = models.DateField()
    구분 = models.CharField(max_length=100, blank=True, null=True)  # 추가한 부분

    class Meta:
        unique_together = ('UID', '사용일')

    
def calculate_new_visitors():
    return Visitor.objects.filter(구분__in=['신규카드', '신규현금']).count()
