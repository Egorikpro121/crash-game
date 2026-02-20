# Cloudflare Worker vs Pages - Важно!

## Проблема
Вы настроили **Cloudflare Worker**, но для фронтенда нужен **Cloudflare Pages**!

## Разница

### Cloudflare Worker
- Для серверных функций (API endpoints, обработка запросов)
- Не подходит для статических сайтов (React/Vite)
- Использует `wrangler deploy`

### Cloudflare Pages
- Для статических сайтов (React, Vue, Vite, и т.д.)
- Идеально для Telegram Mini Apps
- Автоматический деплой из Git
- Бесплатный HTTPS

---

## Решение: Создать Cloudflare Pages проект

### Шаг 1: Создайте новый Pages проект

1. Зайдите в **Cloudflare Dashboard**
2. Выберите **Pages** (не Workers!)
3. Нажмите **"Create a project"**
4. Выберите **"Connect to Git"**
5. Выберите репозиторий: `Egorikpro121/crash-game`

### Шаг 2: Настройте Build settings

**Framework preset:**
- Выберите **"Vite"** или **"None"**

**Build command:**
```
cd frontend && npm install && npm run build
```

**Build output directory:**
```
frontend/dist
```

**Root directory:**
- Оставьте пустым (или `/`)

### Шаг 3: Environment variables (если нужны)

Добавьте переменные окружения:
- `VITE_API_URL` = URL вашего backend (например, `https://your-backend.com`)

### Шаг 4: Сохраните и дождитесь деплоя

После сохранения Cloudflare автоматически:
1. Клонирует репозиторий
2. Выполнит `cd frontend && npm install && npm run build`
3. Задеплоит результат на `*.pages.dev` домен

---

## Что делать с Worker?

Если вы создали Worker по ошибке:
1. Можете его удалить (он не нужен для фронтенда)
2. Или оставить для будущего использования (например, для проксирования запросов к backend)

---

## Итоговая архитектура

```
┌─────────────────┐
│  Cloudflare     │
│     Pages       │  ← Frontend (React/Vite)
│  *.pages.dev    │
└─────────────────┘
         │
         │ API запросы
         ▼
┌─────────────────┐
│   Backend       │  ← FastAPI (Railway/Render/VPS)
│   (ваш сервер)  │
└─────────────────┘
```

Worker здесь не нужен для фронтенда!
