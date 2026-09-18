# Real-time аналитика событий на ClickHouse

## Описание проекта

Проект представляет собой платформу продуктовой аналитики на основе ClickHouse. Генерируется поток пользовательских событий (просмотры, добавления в корзину, оформления заказов, покупки), загружается в ClickHouse и анализируется с помощью SQL-запросов: DAU, воронки продаж, retention.

## Архитектура

Python Generator -> ClickHouse -> Metabase


## Стек технологий

- **ClickHouse 24.3**
- **Python 3.11**
- **Docker**
- **Metabase**

## Структура проекта

```
clickhouse-analytics/
├── docker-compose.yml
├── generator/
│ └── generate_events.py
├── sql/
│ └── analytics_queries.sql
├── screenshots/
├── .gitignore
├── README.md
└──requirements.txt

```


## Как запустить

### Требования

- Docker Desktop
- Python 3.10+
- 8+ ГБ RAM

### Шаги

1. Клонировать репозиторий

   git clone https://github.com/Aleksei185/clickhouse-analytics.git
   cd clickhouse-analytics

2. Запустить контейнеры 

    docker compose up -d

3. Установить зависимости Python

    pip install -r requirements.txt

4. Создать таблицу в ClickHouse

    docker compose exec clickhouse clickhouse-client
    Затем выполнить SQL из sql/analytics_queries.sql

5. Сгенерировать события

    cd generator
    python generate_events.py

6. Открыть Metabase: http://localhost:3000

## Скриншот

![analytics dashboard](product%20analytics%20dashboard.png)

## Автор

Алексей Чвирук, 2026
