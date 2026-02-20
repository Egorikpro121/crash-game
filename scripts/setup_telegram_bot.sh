#!/bin/bash
# Скрипт для настройки Telegram бота

set -e

echo "=========================================="
echo "Telegram Bot Setup Script"
echo "=========================================="
echo ""

# Проверка наличия токена
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  TELEGRAM_BOT_TOKEN не установлен"
    echo "Получите токен у @BotFather в Telegram"
    read -p "Введите токен бота: " BOT_TOKEN
    export TELEGRAM_BOT_TOKEN=$BOT_TOKEN
fi

# Проверка наличия URL
if [ -z "$WEBHOOK_URL" ]; then
    echo "⚠️  WEBHOOK_URL не установлен"
    read -p "Введите URL вашего Mini App (например: https://yourdomain.com): " WEBHOOK_URL
    export WEBHOOK_URL=$WEBHOOK_URL
fi

echo ""
echo "Настройка бота..."
echo ""

# Проверка бота
echo "1. Проверка бота..."
BOT_INFO=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe")
if echo "$BOT_INFO" | grep -q '"ok":true'; then
    BOT_USERNAME=$(echo "$BOT_INFO" | grep -o '"username":"[^"]*' | cut -d'"' -f4)
    echo "   ✓ Бот найден: @${BOT_USERNAME}"
else
    echo "   ✗ Ошибка: Неверный токен бота"
    exit 1
fi

# Установка webhook
echo ""
echo "2. Установка webhook..."
WEBHOOK_RESPONSE=$(curl -s -X POST \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"${WEBHOOK_URL}/webhooks/stars\"}")

if echo "$WEBHOOK_RESPONSE" | grep -q '"ok":true'; then
    echo "   ✓ Webhook установлен: ${WEBHOOK_URL}/webhooks/stars"
else
    echo "   ✗ Ошибка установки webhook:"
    echo "$WEBHOOK_RESPONSE" | grep -o '"description":"[^"]*' | cut -d'"' -f4
fi

# Установка кнопки меню
echo ""
echo "3. Установка кнопки меню..."
MENU_RESPONSE=$(curl -s -X POST \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setChatMenuButton" \
    -H "Content-Type: application/json" \
    -d "{\"menu_button\": {\"type\": \"web_app\", \"text\": \"🎮 Играть\", \"web_app\": {\"url\": \"${WEBHOOK_URL}\"}}}")

if echo "$MENU_RESPONSE" | grep -q '"ok":true'; then
    echo "   ✓ Кнопка меню установлена"
else
    echo "   ⚠️  Не удалось установить кнопку меню (может потребоваться сделать через BotFather)"
fi

# Проверка webhook
echo ""
echo "4. Проверка webhook..."
WEBHOOK_INFO=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo")
echo "$WEBHOOK_INFO" | python3 -m json.tool 2>/dev/null || echo "$WEBHOOK_INFO"

echo ""
echo "=========================================="
echo "✅ Настройка завершена!"
echo "=========================================="
echo ""
echo "Следующие шаги:"
echo "1. Откройте вашего бота в Telegram: @${BOT_USERNAME}"
echo "2. Нажмите на кнопку меню (если видна)"
echo "3. Mini App должна открыться"
echo ""
echo "Если Mini App не открывается:"
echo "- Убедитесь, что URL начинается с https://"
echo "- Проверьте, что сайт доступен"
echo "- Используйте команду /setmenubutton в @BotFather"
