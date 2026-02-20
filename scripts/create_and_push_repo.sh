#!/bin/bash
# Скрипт для создания репозитория на GitHub и загрузки кода

set -e

cd "$(dirname "$0")/.."

echo "=========================================="
echo "GitHub Repository Creation"
echo "=========================================="
echo ""

# Проверка git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен"
    exit 1
fi

# Проверка наличия коммитов
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "❌ Нет коммитов в репозитории"
    exit 1
fi

# Переименование ветки в main если нужно
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Переименование ветки в main..."
    git branch -M main
fi

# Проверка GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI найден"
    
    # Проверка авторизации
    if gh auth status &>/dev/null; then
        echo "✅ Авторизован в GitHub"
        
        # Создание репозитория
        echo ""
        echo "Создание репозитория на GitHub..."
        
        if gh repo create crash-game --public --source=. --remote=origin --push 2>&1; then
            echo ""
            echo "✅ Репозиторий создан и код загружен!"
            echo ""
            echo "URL репозитория:"
            gh repo view --web crash-game 2>/dev/null || echo "https://github.com/$(gh api user --jq .login)/crash-game"
        else
            echo "⚠️  Не удалось создать через GitHub CLI"
            echo "Попробуйте создать репозиторий вручную на GitHub.com"
        fi
    else
        echo "⚠️  Не авторизован в GitHub CLI"
        echo ""
        echo "Авторизуйтесь командой:"
        echo "  gh auth login"
        echo ""
        echo "Или создайте репозиторий вручную на GitHub.com"
    fi
else
    echo "⚠️  GitHub CLI не установлен"
    echo ""
    echo "Установите: sudo apt install gh"
    echo "Или создайте репозиторий вручную на GitHub.com"
fi

echo ""
echo "=========================================="
echo "Если репозиторий уже создан на GitHub:"
echo "=========================================="
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/crash-game.git"
echo "git push -u origin main"
echo ""
