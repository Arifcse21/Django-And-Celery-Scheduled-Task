### Install/setup RabbitMQ with Helm
```bash
helm install rabbitmq bitnami/rabbitmq \
  -n schedule-queue-system \
  -f components/rabbitmq/rabbitmq-values.yaml
```

### Upgrade RabbitMQ with Helm
```bash
helm upgrade rabbitmq bitnami/rabbitmq \
  -n schedule-queue-system \
  -f rabbitmq-values.yaml
```

```bash
kubectl get secret rabbitmq-default-user \
  -n schedule-queue-system \
  -o jsonpath='{.data.username}' | base64 --decode
```

```bash
kubectl get secret rabbitmq-default-user \
  -n schedule-queue-system \
  -o jsonpath='{.data.password}' | base64 --decode
```