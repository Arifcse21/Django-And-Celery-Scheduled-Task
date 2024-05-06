from django.urls import path
from routine_runner.views import *


urlpatterns = [
    path('cronschedule/', CronJobListCreateView.as_view()),
    path('cronschedule/<int:pk>/', CronJobRetrieveView.as_view()),
]
