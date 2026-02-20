# Интеграция Frontend и Backend - Сводка

## ✅ Выполнено

### 1. API Client для Frontend
- Создан `frontend/src/api/client.ts` - полнофункциональный API клиент
- Поддержка аутентификации через JWT токены
- Поддержка Telegram Mini App init data
- Методы для всех основных операций:
  - Auth (login, getMe)
  - Game (round status, place bet, cashout, history)
  - Payments (deposit, withdrawal, history)
  - User (balance, statistics)
  - Bonuses (available, claim)
  - Referrals (code, statistics)
  - Leaderboard (top earners)

### 2. Обновлен Backend API
- Добавлены новые routes в `src/api/main.py`:
  - `/bonuses/*` - бонусная система
  - `/referrals/*` - реферальная система
  - `/leaderboard/*` - рейтинг игроков
- Обновлен CORS для поддержки localhost разработки
- Добавлены недостающие `__init__.py` файлы

### 3. Интеграционные тесты
Создано 4 файла интеграционных тестов:
- `test_api_integration.py` - тесты API endpoints
- `test_economics_flow.py` - тесты экономических потоков
- `test_frontend_backend_integration.py` - тесты интеграции
- `test_basic_functionality.py` - базовые функциональные тесты

### 4. Скрипты для запуска
- `scripts/start_backend.sh` - запуск backend сервера
- `scripts/start_frontend.sh` - запуск frontend dev server
- `scripts/test.sh` - запуск всех тестов

### 5. Конфигурация
- `frontend/.env.example` - пример конфигурации для frontend
- `tests/conftest.py` - конфигурация pytest
- `README_TESTING.md` - руководство по тестированию

## 📁 Структура интеграции

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts          # API клиент
│   ├── pages/                  # Страницы приложения
│   └── components/             # Компоненты игры
│
src/
├── api/
│   ├── main.py                 # Главный FastAPI app
│   └── routes/
│       ├── bonuses/            # Бонусные routes
│       ├── referrals/           # Реферальные routes
│       └── leaderboard/        # Рейтинг routes
│
tests/
└── integration/
    ├── test_api_integration.py
    ├── test_economics_flow.py
    ├── test_frontend_backend_integration.py
    └── test_basic_functionality.py
```

## 🚀 Запуск для тестирования

### Backend
```bash
# Установить зависимости
pip install -r requirements.txt

# Настроить .env
cp .env.example .env
# Отредактировать .env

# Запустить сервер
./scripts/start_backend.sh
# Сервер будет доступен на http://localhost:8000
```

### Frontend
```bash
cd frontend

# Установить зависимости
npm install

# Настроить .env
cp .env.example .env
# VITE_API_URL=http://localhost:8000

# Запустить dev server
npm run dev
# Приложение будет доступно на http://localhost:3000
```

### Тесты
```bash
# Установить pytest
pip install pytest pytest-asyncio httpx

# Запустить тесты
./scripts/test.sh
# или
python3 -m pytest tests/ -v
```

## 🔗 Связь Frontend ↔ Backend

### Аутентификация
1. Frontend получает Telegram user data через `window.Telegram.WebApp.initData`
2. Отправляет на `/auth/login` для получения JWT токена
3. Сохраняет токен в localStorage
4. Использует токен в заголовке `Authorization: Bearer <token>`

### API Calls
Все запросы идут через `apiClient` из `frontend/src/api/client.ts`:
```typescript
import { apiClient } from '@/api/client';

// Пример использования
const balance = await apiClient.getBalance();
const bonuses = await apiClient.getAvailableBonuses('TON');
```

## 📊 Статистика

- **API Client методов**: 15+
- **Интеграционных тестов**: 4 файла
- **Новых API routes**: 3 модуля
- **Скриптов запуска**: 3

## ⚠️ Заметки

1. Для полного тестирования нужно установить зависимости:
   ```bash
   pip install -r requirements.txt
   npm install --prefix frontend
   ```

2. Убедитесь, что переменные окружения настроены в `.env`

3. Для production нужно обновить CORS origins в `src/api/middleware/security.py`

4. Telegram Mini App требует настройки бота и webhook для Stars платежей

## 🎯 Следующие шаги

1. Запустить тесты и исправить найденные ошибки
2. Протестировать реальное подключение frontend к backend
3. Добавить WebSocket подключение для real-time обновлений игры
4. Настроить production окружение
