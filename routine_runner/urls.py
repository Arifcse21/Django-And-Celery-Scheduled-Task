from django.urls import path
from routine_runner.views import *


urlpatterns = [
    path('cronschedule/', CronJobListCreateView.as_view()),
    path('cronschedule/<int:pk>/', CronJobRetrieveView.as_view()),
    path('health/', health_check, name='health'),
    path('ready/', readiness_check, name='ready'),
]
