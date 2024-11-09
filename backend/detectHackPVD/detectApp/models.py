from django.db import models

class ViolationRecord(models.Model):
    video = models.FileField(upload_to='uploaded_videos/')
    violation_article = models.CharField(max_length=300)
    violation_time = models.IntegerField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    uploaded_at = models.DateTimeField(auto_now_add=True)
