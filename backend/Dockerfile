# backend/Dockerfile
FROM python:3.11.3-bullseye as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11.3-bullseye as test
WORKDIR /app
COPY --from=builder /app /app
RUN python manage.py test

FROM python:3.11.3-bullseye as production
WORKDIR /app
COPY --from=builder /app /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
