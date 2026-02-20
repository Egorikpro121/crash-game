# Исправление ошибки сборки Cloudflare Pages

## Проблема
Cloudflare Pages пытается установить Python зависимости из `requirements.txt`, но это frontend проект.

## Решение

### Вариант 1: Настройка через UI (Рекомендуется)

1. Зайдите в Cloudflare Dashboard → **Pages** → ваш проект
2. Нажмите **Settings** → **Builds & deployments**
3. Измените настройки:

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
   / (оставьте пустым или укажите корень)
   ```

4. Нажмите **Save**
5. Нажмите **Retry build**

### Вариант 2: Создать package.json в корне (обходной путь)

Если Cloudflare продолжает пытаться установить Python зависимости, можно создать `package.json` в корне проекта, который будет указывать на frontend:

```json
{
  "name": "crash-game",
  "version": "1.0.0",
  "scripts": {
    "build": "cd frontend && npm install && npm run build"
  }
}
```

Но лучше использовать настройки из UI.

### Вариант 3: Переместить requirements.txt (не рекомендуется)

Можно временно переименовать `requirements.txt` в `requirements.txt.backend`, но это не решит проблему полностью.

---

## Проверка

После настройки:
1. Cloudflare должен выполнить `npm install` в директории `frontend`
2. Затем выполнить `npm run build`
3. Результат должен быть в `frontend/dist`

---

## Дополнительно

Файл `frontend/_redirects` уже создан для правильной работы SPA роутинга.
