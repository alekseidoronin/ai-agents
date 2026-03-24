# Платформа ИИ-агентов

Платформа для развертывания автономных ИИ-агентов, способных выполнять различные бизнес-задачи: создание контент-планов, генерация воронок продаж, аналитика и многое другое.

## Основные технологии

* **Фреймворк:** FastAPI (Python 3.11+)
* **База данных:** PostgreSQL, SQLAlchemy (ORM), Alembic (миграции)
* **Фоновые задачи:** Celery, Redis, APScheduler
* **ИИ интеграции:** OpenAI (GPT-4), Anthropic (Claude)
* **Интерфейс:** Telegram Bot API (python-telegram-bot)
* **Контейнеризация:** Docker, Docker Compose

## Архитектура

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Telegram    │────▶│  FastAPI      │────▶│  AI Agents      │
│  Bot         │     │  (REST API)  │     │  (GPT-4/Claude) │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
                    ┌──────┴───────┐
                    │              │
              ┌─────▼─────┐ ┌─────▼─────┐
              │ PostgreSQL │ │   Redis    │
              │ (данные)   │ │ (очереди)  │
              └───────────┘ └─────┬─────┘
                                  │
                           ┌──────▼──────┐
                           │   Celery    │
                           │  (воркеры)  │
                           └─────────────┘
```

## Структура проекта

```
app/
├── agents/                 — ИИ-агенты (паттерн Strategy)
│   ├── base.py             — базовый класс BaseAgent
│   ├── content_plan_agent.py
│   ├── sales_funnel_agent.py
│   └── analytics_agent.py
├── models/                 — модели SQLAlchemy
│   ├── user.py             — пользователи
│   ├── content_plan.py     — контент-планы
│   ├── sales_funnel.py     — воронки продаж
│   └── session.py          — сессии агентов
├── schemas/                — Pydantic-схемы (валидация)
│   ├── user.py
│   ├── content_plan.py
│   ├── sales_funnel.py
│   └── session.py
├── routers/                — HTTP-эндпоинты
│   ├── users.py
│   ├── content_plans.py
│   └── sales_funnels.py
├── services/               — бизнес-логика
│   ├── ai_service.py       — фасад над агентами
│   └── telegram_bot.py     — Telegram-бот
├── middleware/              — промежуточное ПО
│   └── error_handler.py
├── tasks/                  — Celery-задачи
│   └── ai_tasks.py
├── prompts/                — шаблоны промптов
│   ├── content_plan.txt
│   ├── sales_funnel.txt
│   └── analytics.txt
├── utils/                  — утилиты
├── config.py               — настройки (Pydantic Settings)
├── database.py             — подключение к БД
├── celery_app.py           — конфигурация Celery
└── main.py                 — точка входа FastAPI
migrations/                 — Alembic-миграции
tests/                      — тесты
docker-compose.yml          — оркестрация сервисов
Dockerfile                  — образ приложения
```

## Установка и запуск

### Локальная разработка

1.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    pip install ruff pytest pytest-asyncio httpx
    ```

2.  **Настройте переменные окружения:**
    ```bash
    cp .env.example .env
    # Заполните .env своими ключами
    ```

3.  **Запустите PostgreSQL и Redis** (или используйте Docker):
    ```bash
    sudo pg_ctlcluster 16 main start
    sudo service redis-server start
    ```

4.  **Запустите приложение:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Docker

```bash
docker-compose up --build
```

## API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/` | Статус платформы |
| GET | `/health` | Проверка здоровья |
| GET | `/docs` | Swagger UI |
| GET/POST | `/api/users/` | Пользователи |
| GET/POST/DELETE | `/api/content-plans/` | Контент-планы |
| GET/POST/DELETE | `/api/sales-funnels/` | Воронки продаж |

## Команды

* **Линтер:** `ruff check .`
* **Тесты:** `pytest tests/ -v`
* **Миграции:** `alembic revision --autogenerate -m "описание"` / `alembic upgrade head`
* **Celery:** `celery -A app.celery_app worker --loglevel=info`
