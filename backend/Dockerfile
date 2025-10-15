FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh ./
RUN python - <<'PY'
p = '/app/entrypoint.sh'
data = open(p, 'rb').read()
# убрать UTF-8 BOM
if data.startswith(b'\xef\xbb\xbf'):
    data = data[3:]
# нормализовать переводы строк
data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
# заменить дефисы (en dash/em dash/minus) на ASCII "-"
for ch in ('–', '—', '−'):
    data = data.replace(ch.encode('utf-8'), b'-')
open(p, 'wb').write(data)
PY
RUN chmod +x /app/entrypoint.sh

COPY ../.. .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
