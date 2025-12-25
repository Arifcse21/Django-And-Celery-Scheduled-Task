FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=scheduler_core.settings

WORKDIR /app

COPY . .
RUN pip install  -r requirements.txt
RUN python manage.py migrate --noinput


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]