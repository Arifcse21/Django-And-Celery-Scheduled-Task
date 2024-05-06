from rest_framework import serializers
from routine_runner.models import CronJobModel


class CronJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CronJobModel
        fields = '__all__'
        read_only_fields = [
            "cronsched", "is_executed", "resp_msg", 
            "created_at", "updated_at"
        ]