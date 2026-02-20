# 🚀 Быстрый старт - Подключение Mini App в Telegram

## ⚡ За 10 минут

### Шаг 1: Создайте бота (2 минуты)

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Введите имя и username бота
4. **Скопируйте токен** - он понадобится

### Шаг 2: Получите бесплатный домен (3 минуты)

#### Вариант A: Vercel (Самый простой)
1. Зайдите на https://vercel.com
2. Войдите через GitHub
3. New Project → Import Git Repository
4. Выберите ваш репозиторий
5. Настройки:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/dist`
6. Deploy
7. **Готово!** Домен: `your-project.vercel.app`

#### Вариант B: Cloudflare Pages
1. Зайдите на https://pages.cloudflare.com
2. Connect to Git → GitHub
3. Выберите репозиторий
4. Build settings:
   - Framework: Vite
   - Build command: `cd frontend && npm run build`
   - Build output directory: `frontend/dist`
5. Save and Deploy
6. **Готово!** Домен: `your-project.pages.dev`

### Шаг 3: Настройте бота (2 минуты)

#### Через BotFather:
```
/setmenubutton
[Выберите вашего бота]
[Текст: 🎮 Играть]
[URL: https://your-project.vercel.app]
```

#### Или через скрипт:
```bash
export TELEGRAM_BOT_TOKEN=your_token_here
export WEBHOOK_URL=https://your-project.vercel.app
./scripts/setup_telegram_bot.sh
```

### Шаг 4: Проверьте (1 минута)

1. Откройте вашего бота в Telegram
2. Нажмите кнопку меню (три линии внизу)
3. Mini App должна открыться! 🎉

---

## 📝 Для Production (с собственным доменом)

### Купить домен

**Дешевые варианты:**
- Namecheap: ~$10/год (.com)
- REG.RU: ~300₽/год (.ru)
- Cloudflare Registrar: ~$8/год (без наценки)

### Настроить DNS

В настройках домена добавьте:

**Для Vercel:**
```
Тип: CNAME
Имя: www
Значение: cname.vercel-dns.com
```

**Для Cloudflare Pages:**
```
Тип: CNAME
Имя: www
Значение: your-project.pages.dev
```

### Добавить домен в Vercel/Cloudflare

- В настройках проекта → Domains → Add Domain
- Введите ваш домен
- SSL настроится автоматически

---

## 🔧 Настройка Backend

### Railway (Рекомендуется)

1. Зайдите на https://railway.app
2. New Project → Deploy from GitHub
3. Выберите репозиторий
4. Добавьте переменные:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://...
   TELEGRAM_BOT_TOKEN=your-bot-token
   FRONTEND_URL=https://yourdomain.com
   ```
5. Railway создаст домен автоматически

### Обновить Frontend

В `frontend/.env`:
```bash
VITE_API_URL=https://your-backend.railway.app
```

Пересоберите и задеплойте frontend.

---

## ✅ Чеклист

- [ ] Бот создан через BotFather
- [ ] Токен бота сохранен
- [ ] Frontend задеплоен (Vercel/Cloudflare)
- [ ] Backend задеплоен (Railway/Render)
- [ ] Кнопка меню настроена в боте
- [ ] Mini App открывается в Telegram
- [ ] SSL работает (HTTPS)
- [ ] Переменные окружения настроены

---

## 🆘 Проблемы?

### Mini App не открывается
- Проверьте URL в BotFather (должен быть `https://`)
- Убедитесь, что сайт доступен в браузере
- Проверьте, что SSL работает

### Ошибка подключения к API
- Проверьте `VITE_API_URL` в frontend
- Убедитесь, что backend доступен
- Проверьте CORS настройки

### Бот не отвечает
- Проверьте токен бота
- Убедитесь, что webhook настроен
- Проверьте логи backend

---

## 📞 Полезные ссылки

- [BotFather](https://t.me/BotFather) - создание ботов
- [Vercel](https://vercel.com) - хостинг frontend
- [Railway](https://railway.app) - хостинг backend
- [Cloudflare Pages](https://pages.cloudflare.com) - альтернатива Vercel
- [Telegram Bot API](https://core.telegram.org/bots/api) - документация
