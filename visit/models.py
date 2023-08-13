from django.db import models

# Create your models here.

class Visitor(models.Model):
    UID = models.CharField(max_length=200)
    사용일 = models.DateField()
    
    class Meta:
        unique_together = ('UID', '사용일')