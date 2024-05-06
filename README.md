# Scheduled-Task-With-Django-Celery

### Run RabbitMQ
```
docker run -d \
    --name rabbitmq \
    --restart unless-stopped \
    -p 1883:1883 \
    -p 5672:5672 \
    -p 15672:15672 \
    -p 1885:15675 \
    -e RABBITMQ_DEFAULT_USER=$RABBITMQ_DEFAULT_USER \
    -e RABBITMQ_DEFAULT_PASS=$RABBITMQ_DEFAULT_PASS \
    rabbitmq:3.12-management \
    sh -c "printenv && \
    rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_web_mqtt rabbitmq_amqp1_0 && \
    rabbitmq-server"
```


### Run celery worker
```
celery -A scheduler_core  worker -l INFO -E
```

### Celery flower
```
celery --broker=amqp://$RABBITMQ_DEFAULT_USER:$RABBITMQ_DEFAULT_PASS@$RABBITMQ_HOST:$RABBITMQ_PORT/ flower --port=$FLOWER_PORT --basic-auth=$FLOWER_USER:$FLOWER_PASS
```

### Celery Beat
```
celery -A scheduler_core beat -l INFO --scheduler django_celery_beat.schedulers.DatabaseScheduler
```