# Как создать Cloudflare Pages проект (не Worker!)

## Проблема
Когда вы нажимаете "Create application", видите только опцию создать Worker, но для фронтенда нужен **Pages**.

## Решение: Перейдите в раздел Pages

### Шаг 1: Найдите раздел Pages

1. В левом меню Cloudflare Dashboard найдите раздел **"Pages"**
   - Обычно он находится рядом с "Workers & Pages"
   - Или в списке продуктов: "Workers", "Pages", "R2", и т.д.

2. **Нажмите на "Pages"** (не "Workers & Pages"!)

### Шаг 2: Создайте Pages проект

1. В разделе Pages нажмите **"Create a project"** (синяя кнопка справа вверху)
2. Выберите **"Connect to Git"**
3. Авторизуйтесь через GitHub (если еще не авторизованы)
4. Выберите репозиторий: **`Egorikpro121/crash-game`**
5. Нажмите **"Begin setup"**

### Шаг 3: Настройте Build settings

В форме настройки укажите:

**Project name:**
```
crash-game
```

**Production branch:**
```
main
```

**Framework preset:**
```
Vite (или выберите "None")
```

**Build command:**
```
cd frontend && npm install && npm run build
```

**Build output directory:**
```
frontend/dist
```

**Root directory:**
```
/ (оставьте пустым)
```

### Шаг 4: Сохраните и задеплойте

1. Нажмите **"Save and Deploy"**
2. Дождитесь завершения сборки (обычно 2-5 минут)
3. После успешного деплоя вы получите домен: `crash-game-xxxxx.pages.dev`

---

## Визуальная разница

### Workers & Pages (общий раздел)
- Показывает и Workers, и Pages проекты
- При создании может предлагать только Worker

### Pages (отдельный раздел)
- Только для статических сайтов
- Идеально для React/Vite фронтенда
- При создании предлагает подключить Git репозиторий

---

## Если не можете найти Pages

1. В левом меню прокрутите вниз
2. Ищите в разделе "Products" или "Developers"
3. Или используйте поиск вверху: введите "Pages"

---

## Альтернатива: Прямая ссылка

Попробуйте открыть напрямую:
```
https://dash.cloudflare.com/[ваш-account-id]/pages
```

Или через меню:
**Dashboard → Pages → Create a project**

---

## Важно!

- ✅ **Pages** = для фронтенда (React, Vite, статические сайты)
- ❌ **Worker** = для серверных функций (API endpoints)

Для Telegram Mini App нужен **Pages**, не Worker!
