# Testing Guide

## Запуск тестов

### Backend тесты

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить все тесты
python3 -m pytest tests/ -v

# Запустить конкретный тест
python3 -m pytest tests/integration/test_api_integration.py -v

# Запустить с покрытием
python3 -m pytest tests/ --cov=src --cov-report=html
```

### Frontend тесты

```bash
cd frontend
npm install
npm test
```

## Интеграционное тестирование

### Запуск backend сервера

```bash
# Установить переменные окружения
cp .env.example .env
# Отредактировать .env

# Запустить сервер
./scripts/start_backend.sh
# или
uvicorn src.api.main:app --reload
```

### Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

### Тестирование API

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"telegram_user_id": 123456789, "username": "test"}'

# Get balance (с токеном)
curl http://localhost:8000/user/balance \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Структура тестов

- `tests/integration/` - Интеграционные тесты
  - `test_api_integration.py` - Тесты API endpoints
  - `test_economics_flow.py` - Тесты экономических потоков
  - `test_frontend_backend_integration.py` - Тесты интеграции frontend-backend
  - `test_basic_functionality.py` - Базовые функциональные тесты

## Переменные окружения для тестов

```bash
export SECRET_KEY="test-secret-key-for-testing-only"
export DATABASE_URL="sqlite:///./test.db"
```
