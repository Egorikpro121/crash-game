# Исправление ошибки сборки Cloudflare Pages

## Текущая ситуация
✅ Репозиторий подключен: `Egorikpro121/crash-game`  
❌ Сборка падает: "Latest build failed"

## Что нужно сделать

### Шаг 1: Откройте проект в Cloudflare

1. Нажмите на **`crash-game`** в списке приложений
2. Перейдите в **"Settings"** → **"Builds & deployments"**

### Шаг 2: Проверьте настройки сборки

Убедитесь, что указаны **правильные** настройки:

#### Если это Cloudflare Pages (правильно):
```
Framework preset: Vite (или None)

Build command:
cd frontend && npm install && npm run build

Build output directory:
frontend/dist

Root directory:
/ (оставьте пустым)
```

#### Если это Cloudflare Worker (неправильно):
Нужно пересоздать как **Pages** проект!

### Шаг 3: Проверьте логи сборки

1. В проекте перейдите на вкладку **"Deployments"**
2. Откройте последний failed deployment
3. Посмотрите логи - там будет указана точная ошибка

### Шаг 4: Возможные проблемы и решения

#### Проблема 1: "npm: command not found"
**Решение:** Cloudflare автоматически установит Node.js, но убедитесь, что используете Pages, а не Worker.

#### Проблема 2: "Cannot find module"
**Решение:** Проверьте, что `frontend/package.json` существует и содержит все зависимости.

#### Проблема 3: "Build output directory not found"
**Решение:** Убедитесь, что указан правильный путь: `frontend/dist`

#### Проблема 4: Worker вместо Pages
**Решение:** Удалите Worker проект и создайте новый **Pages** проект.

---

## Быстрая проверка

Выполните локально, чтобы убедиться, что сборка работает:

```bash
cd frontend
npm install
npm run build
```

Если локально работает, значит проблема в настройках Cloudflare.

---

## Если ничего не помогает

1. Удалите текущий проект `crash-game` в Cloudflare
2. Создайте новый **Pages** проект (не Worker!)
3. Подключите репозиторий заново
4. Укажите правильные настройки сборки

---

## После успешной сборки

Вы получите домен вида: `crash-game-xxxxx.pages.dev`

Этот домен нужно будет указать в настройках Telegram Bot для Mini App.
