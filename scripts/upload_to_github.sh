#!/bin/bash
# Скрипт для загрузки проекта в GitHub

set -e

echo "=========================================="
echo "GitHub Upload Script"
echo "=========================================="
echo ""

# Проверка git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите: sudo apt install git"
    exit 1
fi

cd "$(dirname "$0")/.."

# Проверка, инициализирован ли git
if [ ! -d ".git" ]; then
    echo "Инициализация git репозитория..."
    git init
fi

# Проверка .gitignore
if [ ! -f ".gitignore" ]; then
    echo "⚠️  .gitignore не найден. Создаю..."
    cat > .gitignore << EOF
# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
frontend/dist/
frontend/build/

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test
test.db
test_*.db
*.log
EOF
fi

# Проверка remote
if git remote -v | grep -q "origin"; then
    echo "Remote 'origin' уже настроен:"
    git remote -v
    read -p "Изменить URL? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Введите новый URL GitHub репозитория: " REPO_URL
        git remote set-url origin "$REPO_URL"
    fi
else
    read -p "Введите URL GitHub репозитория (https://github.com/USERNAME/REPO.git): " REPO_URL
    git remote add origin "$REPO_URL"
fi

# Добавление файлов
echo ""
echo "Добавление файлов..."
git add .

# Проверка изменений
if git diff --cached --quiet; then
    echo "Нет изменений для коммита"
else
    # Коммит
    echo ""
    read -p "Введите сообщение коммита (или Enter для 'Initial commit'): " COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"Initial commit"}
    git commit -m "$COMMIT_MSG"
    
    # Push
    echo ""
    echo "Загрузка в GitHub..."
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
    
    if git ls-remote --heads origin "$CURRENT_BRANCH" | grep -q "$CURRENT_BRANCH"; then
        echo "Ветка $CURRENT_BRANCH уже существует на GitHub"
        read -p "Перезаписать? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push -u origin "$CURRENT_BRANCH" --force
        else
            git push -u origin "$CURRENT_BRANCH"
        fi
    else
        git push -u origin "$CURRENT_BRANCH"
    fi
    
    echo ""
    echo "✅ Проект загружен в GitHub!"
    echo ""
    echo "Следующие шаги:"
    echo "1. Перейдите в Cloudflare Pages"
    echo "2. Подключите этот репозиторий"
    echo "3. Задеплойте проект"
fi
