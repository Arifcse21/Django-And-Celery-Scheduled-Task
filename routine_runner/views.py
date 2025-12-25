from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from routine_runner.models import CronJobModel
from routine_runner.serializers import CronJobSerializer
# Create your views here.


class CronJobListCreateView(generics.ListCreateAPIView):
    queryset = CronJobModel.objects.all()
    serializer_class = CronJobSerializer


class CronJobRetrieveView(generics.RetrieveAPIView):
    queryset = CronJobModel.objects.all()
    serializer_class = CronJobSerializer


def health_check(request):
    """Liveness probe - is the app running?"""
    return JsonResponse({"status": "healthy"}, status=200)

def readiness_check(request):
    """Readiness probe - is the app ready to serve traffic?"""
    try:
        # Check database connection
        connection.ensure_connection()
        return JsonResponse({"status": "ready"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "not ready", "error": str(e)}, status=503)