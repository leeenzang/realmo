from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# 방문자 정보 저장
class Visitor(models.Model):
    UID = models.CharField(max_length=200)
    사용일 = models.DateField()
    구분 = models.CharField(max_length=100, blank=True, null=True)  # 추가한 부분
    uploaded_filename = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('UID', '사용일')     # 동일한 UID, 사용일 가진 데이터가 두 번 이상 저장되는걸 방지


# 일별 방문자 수 저장
class DailyVisitorCount(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date}: {self.count} visitors"
    

# 구분 필드 값이 신규카드, 신규현금인 방문자 수 반환
def calculate_new_visitors():
    return Visitor.objects.filter(구분__in=['신규카드', '신규현금']).count()


# Visitor 모델에 데이터가 저장될 때마다 호출되는 함수
@receiver(post_save, sender=Visitor)
def update_daily_visitor_count(sender, instance, **kwargs):
    date = instance.사용일
    daily_count, created = DailyVisitorCount.objects.get_or_create(date=date)
    daily_count.count = Visitor.objects.filter(사용일=date).count()
    daily_count.save()