FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь backend в /app
COPY . .


RUN find /app -type f -name "*.sh" -print0 | xargs -0 sed -i 's/\r$//' \
 && chmod +x /app/entrypoint.sh

EXPOSE 8000