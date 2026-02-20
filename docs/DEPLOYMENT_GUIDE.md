# Руководство по развертыванию

## Быстрый старт (5 минут)

### Вариант 1: Бесплатный хостинг (Рекомендуется для начала)

#### Frontend на Vercel
1. Зарегистрируйтесь на https://vercel.com
2. Подключите GitHub репозиторий
3. Настройки:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variables:
     - `VITE_API_URL=https://your-backend.railway.app`
4. Домен будет: `your-project.vercel.app`

#### Backend на Railway
1. Зарегистрируйтесь на https://railway.app
2. New Project → Deploy from GitHub
3. Выберите репозиторий
4. Добавьте переменные окружения:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://...
   TELEGRAM_BOT_TOKEN=your-bot-token
   ```
5. Домен будет: `your-project.railway.app`

### Вариант 2: Собственный домен

#### Шаг 1: Купить домен
- Namecheap: https://namecheap.com (~$10/год)
- GoDaddy: https://godaddy.com (~$12/год)
- REG.RU: https://reg.ru (~300₽/год для .ru)

#### Шаг 2: Настроить DNS

Для Vercel (Frontend):
```
Тип: CNAME
Имя: www
Значение: cname.vercel-dns.com
```

Для Railway (Backend):
```
Тип: CNAME
Имя: api
Значение: your-project.railway.app
```

#### Шаг 3: Добавить домен в Vercel/Railway
- В настройках проекта добавьте ваш домен
- SSL настроится автоматически

---

## Пошаговая инструкция

### 1. Подготовка

```bash
# Клонируйте репозиторий
git clone your-repo
cd your-repo

# Создайте .env файлы
cp .env.example .env
cp frontend/.env.example frontend/.env
```

### 2. Настройка переменных окружения

**Backend (.env):**
```bash
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/dbname
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
FRONTEND_URL=https://yourdomain.com
```

**Frontend (frontend/.env):**
```bash
VITE_API_URL=https://api.yourdomain.com
```

### 3. Деплой Frontend

#### Vercel
```bash
cd frontend
npm install
npm run build

# Установите Vercel CLI
npm i -g vercel

# Деплой
vercel
```

#### Или через GitHub:
1. Push в GitHub
2. Подключите репозиторий в Vercel
3. Автоматический деплой

### 4. Деплой Backend

#### Railway
```bash
# Установите Railway CLI
npm i -g @railway/cli

# Логин
railway login

# Инициализация проекта
railway init

# Деплой
railway up
```

#### Или через GitHub:
1. Push в GitHub
2. Подключите репозиторий в Railway
3. Добавьте переменные окружения
4. Автоматический деплой

### 5. Настройка Telegram бота

```bash
# Сделайте скрипт исполняемым
chmod +x scripts/setup_telegram_bot.sh

# Запустите настройку
export TELEGRAM_BOT_TOKEN=your-token
export WEBHOOK_URL=https://yourdomain.com
./scripts/setup_telegram_bot.sh
```

Или вручную через BotFather:
```
/setmenubutton
[Выберите бота]
[Текст кнопки: Играть]
[URL: https://yourdomain.com]
```

---

## Проверка работоспособности

### 1. Проверка Frontend
```bash
curl https://yourdomain.com
# Должен вернуть HTML страницу
```

### 2. Проверка Backend
```bash
curl https://api.yourdomain.com/health
# Должен вернуть: {"status": "healthy"}
```

### 3. Проверка бота
```bash
curl "https://api.telegram.org/bot<TOKEN>/getMe"
# Должен вернуть информацию о боте
```

### 4. Проверка Mini App
1. Откройте бота в Telegram
2. Нажмите кнопку меню
3. Mini App должна открыться

---

## Troubleshooting

### Mini App не открывается
- ✅ Проверьте, что URL начинается с `https://`
- ✅ Убедитесь, что сайт доступен
- ✅ Проверьте настройки в BotFather

### Webhook не работает
- ✅ Проверьте, что backend доступен по HTTPS
- ✅ Убедитесь, что endpoint `/webhooks/stars` существует
- ✅ Проверьте логи backend

### Ошибки CORS
- ✅ Убедитесь, что в `src/api/middleware/security.py` добавлен ваш домен
- ✅ Проверьте заголовки ответа

---

## Мониторинг

### Логи Railway
```bash
railway logs
```

### Логи Vercel
В панели Vercel → Deployments → View Function Logs

### Мониторинг бота
```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```
