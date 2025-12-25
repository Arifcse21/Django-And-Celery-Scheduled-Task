# Export from Podman
```bash
podman save localhost/django-scheduler:latest -o django-scheduler.tar
```

# Import to K3s
```bash
sudo k3s ctr images import django-scheduler.tar
```

# Verify
```bash
sudo k3s ctr images ls | grep django-scheduler
```