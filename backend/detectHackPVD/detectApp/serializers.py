from rest_framework import serializers
from .models import ViolationRecord

class ViolationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationRecord
        fields = ['id', 'video', 'violation_article', 'violation_time', 'fine_amount', 'uploaded_at']
