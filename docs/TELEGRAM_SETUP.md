# Руководство по подключению Telegram Mini App

## 📋 Содержание

1. [Создание Telegram бота](#1-создание-telegram-бота)
2. [Получение домена](#2-получение-домена)
3. [Настройка SSL сертификата](#3-настройка-ssl-сертификата)
4. [Подключение Mini App](#4-подключение-mini-app)
5. [Настройка Webhook](#5-настройка-webhook)
6. [Настройка Telegram Stars](#6-настройка-telegram-stars)

---

## 1. Создание Telegram бота

### Шаг 1: Получить токен бота

1. Откройте Telegram и найдите бота [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "Crash Game")
   - Введите username бота (должен заканчиваться на `bot`, например: `crash_game_bot`)
4. **Сохраните токен бота** - он понадобится для настройки

### Шаг 2: Настроить бота для Mini App

Отправьте BotFather следующие команды:

```
/setdescription
[Выберите вашего бота]
Описание: Играйте в Crash Game и выигрывайте TON и Stars!
```

```
/setabouttext
[Выберите вашего бота]
О боте: Telegram Mini App для игры Crash Game с поддержкой TON и Telegram Stars
```

```
/setuserpic
[Выберите вашего бота]
[Загрузите иконку бота]
```

---

## 2. Получение домена

### Вариант 1: Бесплатные домены (для разработки)

#### Cloudflare Pages (Рекомендуется)
- **URL**: https://pages.cloudflare.com
- **Бесплатно**: Да
- **SSL**: Автоматически
- **Домен**: `your-project.pages.dev`
- **Поддержка**: Отличная

**Шаги:**
1. Зарегистрируйтесь на Cloudflare
2. Перейдите в Pages → Create a project
3. Подключите GitHub репозиторий или загрузите файлы
4. Домен будет доступен автоматически

#### Vercel
- **URL**: https://vercel.com
- **Бесплатно**: Да
- **SSL**: Автоматически
- **Домен**: `your-project.vercel.app`
- **Поддержка**: Отличная

**Шаги:**
1. Зарегистрируйтесь на Vercel
2. Импортируйте проект из GitHub
3. Домен будет создан автоматически

#### Netlify
- **URL**: https://netlify.com
- **Бесплатно**: Да
- **SSL**: Автоматически
- **Домен**: `your-project.netlify.app`

#### GitHub Pages
- **URL**: https://pages.github.com
- **Бесплатно**: Да
- **SSL**: Автоматически
- **Домен**: `username.github.io/project-name`
- **Ограничение**: Только статические сайты

### Вариант 2: Платные домены (для production)

#### Namecheap
- **Цена**: ~$10-15/год
- **URL**: https://namecheap.com
- **Плюсы**: Недорого, хорошая поддержка

#### GoDaddy
- **Цена**: ~$12-20/год
- **URL**: https://godaddy.com
- **Плюсы**: Популярный, много доменных зон

#### Cloudflare Registrar
- **Цена**: По себестоимости (~$8-10/год)
- **URL**: https://cloudflare.com/products/registrar
- **Плюсы**: Без наценки, автоматический SSL

#### REG.RU (для .ru доменов)
- **Цена**: ~300-500₽/год
- **URL**: https://reg.ru
- **Плюсы**: Локальный регистратор

### Вариант 3: VPS с собственным доменом

Если у вас есть VPS (например, на DigitalOcean, Hetzner, Timeweb):

1. Купите домен у регистратора
2. Настройте DNS записи:
   ```
   A запись: @ → IP вашего VPS
   A запись: www → IP вашего VPS
   ```
3. Установите Nginx/Apache на VPS
4. Настройте SSL через Let's Encrypt (бесплатно)

---

## 3. Настройка SSL сертификата

### Для Cloudflare/Vercel/Netlify
SSL настраивается автоматически - ничего делать не нужно!

### Для собственного VPS

#### Использование Let's Encrypt (бесплатно)

**С Certbot:**
```bash
# Установка Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Автоматическое обновление (добавится в cron)
```

**С Docker:**
```bash
docker run -it --rm \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt \
  certbot/certbot certonly --standalone \
  -d yourdomain.com -d www.yourdomain.com
```

---

## 4. Подключение Mini App

### Шаг 1: Настроить бота через BotFather

Отправьте BotFather:

```
/newapp
[Выберите вашего бота]
[Введите название Mini App]
[Введите описание]
[Загрузите иконку 640x360px]
[Введите короткое название]
```

Затем:

```
/setmenubutton
[Выберите вашего бота]
[Введите текст кнопки, например: "Играть"]
[Введите URL вашего Mini App: https://yourdomain.com]
```

### Шаг 2: Настроить кнопку меню

Альтернативно, можно добавить кнопку через код бота:

```python
from telegram import Bot, MenuButtonWebApp, WebAppInfo

bot = Bot(token="YOUR_BOT_TOKEN")

# Установить кнопку меню
bot.set_chat_menu_button(
    menu_button=MenuButtonWebApp(
        text="🎮 Играть",
        web_app=WebAppInfo(url="https://yourdomain.com")
    )
)
```

### Шаг 3: Обновить frontend для работы с Telegram

В `frontend/src/main.tsx` добавьте проверку Telegram WebApp:

```typescript
// Проверка, что мы в Telegram
if (window.Telegram?.WebApp) {
  const tg = window.Telegram.WebApp;
  tg.ready();
  tg.expand();
  
  // Включить закрывающую кнопку
  tg.enableClosingConfirmation();
}
```

---

## 5. Настройка Webhook

### Для получения платежей Telegram Stars

Создайте файл `src/api/routes/stars/webhook.py`:

```python
from fastapi import APIRouter, Request, HTTPException
from src.payments.stars.webhook import process_stars_webhook

router = APIRouter(prefix="/webhooks/stars", tags=["webhooks"])

@router.post("")
async def stars_webhook(request: Request):
    """Handle Telegram Stars webhook."""
    data = await request.json()
    return await process_stars_webhook(data)
```

### Настройка webhook через Bot API

```python
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
WEBHOOK_URL = "https://yourdomain.com/webhooks/stars"

# Установить webhook
response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL}
)

print(response.json())
```

Или через curl:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://yourdomain.com/webhooks/stars"}'
```

---

## 6. Настройка Telegram Stars

### Шаг 1: Включить Stars в боте

Отправьте BotFather:

```
/setstars
[Выберите вашего бота]
[Включите Stars]
```

### Шаг 2: Настроить платежи в коде

В вашем frontend коде используйте Telegram Stars API:

```typescript
// Создание инвойса
const invoice = await apiClient.createDeposit(amount, 'STARS', 'STARS');

// Открытие платежного окна Telegram
if (window.Telegram?.WebApp) {
  window.Telegram.WebApp.openInvoice(invoice.invoice_url, (status) => {
    if (status === 'paid') {
      // Обработка успешного платежа
      console.log('Payment successful!');
    }
  });
}
```

---

## 7. Настройка переменных окружения

Создайте `.env` файл:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_SECRET=your_webhook_secret

# Frontend URL
FRONTEND_URL=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/crash_game

# Security
SECRET_KEY=your_secret_key_here

# TON
TON_API_KEY=your_ton_api_key
TON_WALLET_MNEMONIC=your_wallet_mnemonic
```

---

## 8. Деплой приложения

### Frontend (Vercel/Netlify)

1. Подключите GitHub репозиторий
2. Настройте build команду:
   ```bash
   cd frontend && npm install && npm run build
   ```
3. Укажите output directory: `frontend/dist`
4. Добавьте переменные окружения:
   - `VITE_API_URL=https://api.yourdomain.com`

### Backend (VPS/Railway/Render)

#### Вариант 1: Railway (Рекомендуется для начала)
- **URL**: https://railway.app
- **Бесплатно**: $5 кредитов в месяц
- **Простота**: Очень просто

**Шаги:**
1. Зарегистрируйтесь на Railway
2. New Project → Deploy from GitHub
3. Выберите ваш репозиторий
4. Railway автоматически определит Python проект
5. Добавьте переменные окружения
6. Получите домен: `your-project.railway.app`

#### Вариант 2: Render
- **URL**: https://render.com
- **Бесплатно**: Да (с ограничениями)
- **Домен**: `your-project.onrender.com`

#### Вариант 3: VPS (DigitalOcean, Hetzner)

```bash
# Установка зависимостей
sudo apt update
sudo apt install python3-pip nginx certbot

# Клонирование проекта
git clone your-repo
cd your-repo

# Установка Python зависимостей
pip3 install -r requirements.txt

# Настройка systemd service
sudo nano /etc/systemd/system/crash-game.service
```

Содержимое файла:
```ini
[Unit]
Description=Crash Game API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Запуск:
```bash
sudo systemctl enable crash-game
sudo systemctl start crash-game
```

Настройка Nginx:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 9. Проверка подключения

### Тест 1: Проверка бота
```bash
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe
```

### Тест 2: Проверка webhook
```bash
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

### Тест 3: Проверка Mini App
1. Откройте вашего бота в Telegram
2. Нажмите на кнопку меню
3. Mini App должна открыться

---

## 10. Полезные команды BotFather

```
/mybots - Список ваших ботов
/setdescription - Изменить описание
/setabouttext - Изменить "О боте"
/setuserpic - Изменить фото бота
/setmenubutton - Настроить кнопку меню
/newapp - Создать Mini App
/setstars - Настроить Telegram Stars
```

---

## 📝 Чеклист развертывания

- [ ] Создан бот через BotFather
- [ ] Получен токен бота
- [ ] Выбран и настроен домен
- [ ] Настроен SSL сертификат
- [ ] Frontend задеплоен и доступен по HTTPS
- [ ] Backend задеплоен и доступен по HTTPS
- [ ] Настроена кнопка меню в боте
- [ ] Mini App открывается в Telegram
- [ ] Настроен webhook для Stars
- [ ] Протестированы платежи
- [ ] Добавлены переменные окружения

---

## 🔗 Полезные ссылки

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- [Telegram Stars](https://core.telegram.org/bots/payments)
- [BotFather](https://t.me/BotFather)
- [Cloudflare Pages](https://pages.cloudflare.com)
- [Vercel](https://vercel.com)
- [Railway](https://railway.app)

---

## 💡 Рекомендации

1. **Для разработки**: Используйте Cloudflare Pages (frontend) + Railway (backend)
2. **Для production**: Собственный домен + VPS или Railway/Render
3. **SSL**: Всегда используйте HTTPS (обязательно для Telegram Mini Apps)
4. **Безопасность**: Храните токены в переменных окружения, не коммитьте в Git
5. **Мониторинг**: Настройте логирование и мониторинг ошибок
