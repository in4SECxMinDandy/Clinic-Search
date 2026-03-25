# Notification Service Dockerfile
FROM python:3.12.13-slim-bookworm@sha256:31c0807da611e2e377a2e9b566ad4eb038ac5a5838cbbbe6f2262259b5dc77a0
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY services/notification-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared/ ./shared/
COPY services/notification-service/ ./notification_service/
EXPOSE 8005
CMD ["uvicorn", "notification_service.main:app", "--host", "0.0.0.0", "--port", "8005"]
