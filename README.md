# 🦸‍♂️ Superhero API

Асинхронное FastAPI-приложение для получения и управления супергероями с использованием внешнего API и собственной базы данных

### 🚀 Возможности
Добавление супергероев по имени через внешнее API

Обработка дубликатов и ошибок API

Фильтрация героев по параметрам: intelligence, strength, speed, power

Поддержка асинхронной работы с БД через SQLAlchemy

Покрытие логики unit-тестами

### 🛠️ Стек технологий
- Python 3.12 
- FastAPI
- QLAlchemy 2.0 (async)
- PostgreSQL
- Alembic
- Docker, Docker Compose
- Pytest (включая pytest-asyncio)
- Ruff (линтер + форматтер)

### 📦 Установка и запуск
```bash
git clone https://github.com/mletunenko/hello_world_test.git
cd hello_world_test
docker-compose up --build
```

### 📚 Документация API
___
```
POST /hero/
```
Создать супергероя по имени (поиск через внешнее API).

Пример тела запроса:

```json
{
  "name": "Maverick"
}
```
____
```
GET /hero
```
 
Получить список героев с фильтрацией.

**Поддерживаемые параметры**:
- name: точное совпадение
- intelligence_eq, intelligence_gte, intelligence_lte
- strength_eq, strength_gte, strength_lte
- speed_eq, speed_gte, speed_lte
- power_eq, power_gte, power_lte

Пример запроса:

```
/hero/?strength_gte=80&intelligence_lte=90
```

### 🧪 Тестирование
``` bash
pytest .
```

### 📌 Заметки 
- Внешнее API: https://superheroapi.com
- Ключ API берётся из .env 
- Все данные сохраняются в PostgreSQL через асинхронную ORM

