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

    