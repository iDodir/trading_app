```bash
alembic init migrations
alembic revision --autogenerate -m "message text"
alembic upgrade head
```

```bash
docker-compose -f docker-compose-local.yaml up -d
```

```bash
celery -A src.tasks.tasks:celery worker --loglevel=INFO
```

```bash
celery -A src.tasks.tasks:celery flower
```
