# backend/Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]