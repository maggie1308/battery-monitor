# Battery Monitor 

Сервис мониторинга аккумуляторных батарей.

- Сущности: **Device (Устройство)**, **Battery (АКБ)**
- Связь: устройство ↔ АКБ (many-to-many), ограничение: **не более 5 АКБ** на устройство
- Технологии: Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL 15, HTML/JS, Docker Compose

---

##  Старт

### Предусловия
- Установлен **Docker Desktop** (Windows/macOS) или Docker Engine (Linux).
- На Windows включён WSL2.
- Свободны порты: `8000` (API/UI), `5432` (PostgreSQL).

### Запуск

Убедитесь, что в \battery-monitor\backend\entrypoint.sh - Последивательность конца строки - LF, а не CRLF
```bash
git clone https://github.com/maggie1308/battery-monitor.git
cd battery-monitor  
copy .env.example .env
docker compose up --build
```
Откройте в браузере:
- Ping: `http://localhost:8000` → `{"service":"battery-monitor","status":"ok"}`
- Swagger: `http://localhost:8000/docs`
- UI: `http://localhost:8000/ui`

### Остановка
```bash
docker compose down
```
Полный сброс (удалит том с данными БД):
```bash
docker compose down -v
```

---

##  База данных и миграции

- Модели описаны в **SQLAlchemy** (`backend/app/models.py`).
- Схема создаётся/обновляется **Alembic**-миграциями при старте API автоматически.

Ручные команды :
```bash
# внутри docker-compose окружения
docker compose exec api alembic revision --autogenerate -m "message"
docker compose exec api alembic upgrade head
```

---

## API

Все ответы — **JSON**. Полная спецификация и тестирование — в Swagger на `/docs`.

### Devices
- `GET /devices` — список
- `POST /devices` — создать
  ```json
  { "name":"dev-001", "firmware_version":"1.0.0", "is_on":true }
  ```
- `GET /devices/{id}` — объект + связанные `batteries`
- `PATCH /devices/{id}` / `PUT /devices/{id}` — обновить
- `DELETE /devices/{id}` — удалить (204)

### Batteries
- `GET /batteries` — список
- `POST /batteries` — создать
  ```json
  { "name":"akb-001", "nominal_voltage":12.0, "remaining_capacity":85.5, "service_life_months":36 }
  ```
- `GET /batteries/{id}` — объект + связанные `devices`
- `PATCH /batteries/{id}` / `PUT /batteries/{id}` — обновить
- `DELETE /batteries/{id}` — удалить (204)

### Links (связи устройство ↔ АКБ)
- `POST /devices/{device_id}/batteries/{battery_id}` — привязать  
   при 6-й АКБ вернётся `400 {"detail":"device already has 5 batteries"}`
- `DELETE /devices/{device_id}/batteries/{battery_id}` — отвязать (204)
- `GET /devices/{device_id}/batteries` — список АКБ у устройства

---

## UI

Маршрут: `http://localhost:8000/ui`  
Функциональность:
- создание устройств/АКБ,
- связывание через выпадающие списки (без ручного ввода ID),
- просмотр и отвязка АКБ у выбранного устройства,
- кнопки **Вкл/Выкл** и **Удалить** у устройств, удаление АКБ,
- в списке устройств — колонка **АКБ (IDs)**.

---

## Примеры запросов (Windows)

```powershell
# создать устройство
Invoke-RestMethod -Method POST -Uri http://localhost:8000/devices -ContentType "application/json" `
  -Body '{"name":"dev-001","firmware_version":"1.0.0","is_on":true}'

# создать АКБ
Invoke-RestMethod -Method POST -Uri http://localhost:8000/batteries -ContentType "application/json" `
  -Body '{"name":"akb-001","nominal_voltage":12.0,"remaining_capacity":85.5,"service_life_months":36}'

# связать устройство 1 и АКБ 1
Invoke-RestMethod -Method POST -Uri http://localhost:8000/devices/1/batteries/1

# посмотреть АКБ у устройства 1
Invoke-RestMethod http://localhost:8000/devices/1/batteries
```

---

## Структура проекта

```
backend/
  app/
    __init__.py
    main.py          # FastAPI app + статика /ui
    models.py        # SQLAlchemy модели (Device, Battery, device_battery)
    schemas.py       # Pydantic-схемы
    routers/
      devices.py     # CRUD устройств
      batteries.py   # CRUD АКБ
      links.py       # Привязка/отвязка, список АКБ у устройства
    static/          # UI: index.html, script.js
  Dockerfile
  entrypoint.sh      # ожидание БД, alembic upgrade, запуск uvicorn
alembic/
  versions/          # миграции
alembic.ini
docker-compose.yml
.env.example
README.md
```

---


## Чек-лист по ТЗ
- [x] Модели БД (Device, Battery) и связь many-to-many
- [x] CRUD REST API (JSON) для обеих сущностей
- [x] Добавление/удаление связи АКБ↔Устройство, лимит ≤ 5
- [x] UI (HTML/JS)
- [x] Запуск через `docker-compose.yml`, миграции автоматически
- [x] README с рабочей инструкцией

---

