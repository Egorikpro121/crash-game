#!/bin/bash
# Создание репозитория через GitHub API с токеном

set -e

cd "$(dirname "$0")/.."

echo "=========================================="
echo "GitHub Repository Creation (API)"
echo "=========================================="
echo ""

# Проверка токена
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN не установлен"
    echo ""
    echo "Получите токен:"
    echo "1. GitHub → Settings → Developer settings → Personal access tokens"
    echo "2. Generate new token (classic)"
    echo "3. Выберите scope: repo"
    echo ""
    read -p "Введите GitHub токен: " GITHUB_TOKEN
    export GITHUB_TOKEN
fi

# Получение username
echo "Получение информации о пользователе..."
# Пробуем Bearer формат (для fine-grained tokens)
USERNAME=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user | grep -o '"login":"[^"]*' | cut -d'"' -f4)
# Если не сработало, пробуем token формат
if [ -z "$USERNAME" ]; then
    USERNAME=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep -o '"login":"[^"]*' | cut -d'"' -f4)
fi

if [ -z "$USERNAME" ]; then
    echo "❌ Не удалось получить username. Проверьте токен."
    exit 1
fi

echo "✅ Пользователь: $USERNAME"
echo ""

# Создание репозитория
echo "Создание репозитория 'crash-game'..."
# Пробуем Bearer формат сначала
RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/user/repos \
    -d '{
        "name": "crash-game",
        "description": "Telegram Mini App Crash Game with TON and Stars integration",
        "public": true,
        "auto_init": false
    }')

# Если не сработало, пробуем token формат
if ! echo "$RESPONSE" | grep -q '"name":"crash-game"'; then
    RESPONSE=$(curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d '{
            "name": "crash-game",
            "description": "Telegram Mini App Crash Game with TON and Stars integration",
            "public": true,
            "auto_init": false
        }')
fi

# Проверка результата
if echo "$RESPONSE" | grep -q '"name":"crash-game"'; then
    echo "✅ Репозиторий создан!"
    echo ""
    
    # Настройка remote и push
    echo "Настройка remote..."
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://${GITHUB_TOKEN}@github.com/${USERNAME}/crash-game.git"
    
    echo "Загрузка кода..."
    git branch -M main 2>/dev/null || true
    git push -u origin main
    
    echo ""
    echo "✅ Готово!"
    echo "URL: https://github.com/${USERNAME}/crash-game"
else
    echo "❌ Ошибка создания репозитория:"
    echo "$RESPONSE" | grep -o '"message":"[^"]*' | cut -d'"' -f4 || echo "$RESPONSE"
    exit 1
fi
