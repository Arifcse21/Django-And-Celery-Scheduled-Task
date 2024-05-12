from rest_framework import serializers
from routine_runner.models import CronJobModel
from scheduler_core.celery import app


my_tasks = (
    ("routine_runner.tasks.notify_desktop_task", "Desktop notify"),
    ("routine_runner.tasks.save_joke_task", "Save new joke"),
)


class CronJobSerializer(serializers.ModelSerializer):
    task = serializers.ChoiceField(choices=my_tasks)
    class Meta:
        model = CronJobModel
        fields = '__all__'
        read_only_fields = [
            "cronsched", "clockedsched", "clockedsched_executed", 
            "resp_msg", "created_at", "updated_at"
        ]

    def create(self, validated_data):
        return CronJobModel.objects.create(**validated_data)
    