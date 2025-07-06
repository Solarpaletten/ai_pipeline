#!/bin/bash

# 🔍 Полная проверка Backend AI Pipeline

echo "🔍 ПОЛНАЯ ПРОВЕРКА BACKEND AI PIPELINE"
echo "========================================"
echo ""

# Переходим в корень проекта
cd /var/www/ai_pipeline

echo "📁 Текущая директория: $(pwd)"
echo ""

# 1. Проверяем структуру проекта (исключая frontend)
echo "📂 СТРУКТУРА ПРОЕКТА (без frontend):"
echo "------------------------------------"
find . -maxdepth 2 -type d | grep -v frontend | grep -v node_modules | grep -v __pycache__ | sort
echo ""

# 2. Проверяем основные файлы
echo "📄 ОСНОВНЫЕ ФАЙЛЫ:"
echo "------------------"
ls -la | grep -E "\.(py|yml|yaml|env|json|txt|md)$"
echo ""

# 3. Проверяем Python файлы
echo "🐍 PYTHON ФАЙЛЫ:"
echo "----------------"
find . -name "*.py" | grep -v frontend | head -20
echo ""

# 4. Проверяем Docker конфигурацию
echo "🐳 DOCKER КОНФИГУРАЦИЯ:"
echo "-----------------------"
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml найден"
    echo "Сервисы в docker-compose.yml:"
    grep -A 1 "services:" docker-compose.yml || echo "Не удалось прочитать сервисы"
else
    echo "❌ docker-compose.yml не найден"
fi

if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile найден"
    head -5 Dockerfile
else
    echo "❌ Dockerfile не найден"
fi
echo ""

# 5. Проверяем переменные окружения
echo "⚙️  ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ:"
echo "-------------------------"
if [ -f ".env" ]; then
    echo "✅ .env найден в корне"
    echo "Основные переменные:"
    grep -E "^(API_|TELEGRAM_|ANTHROPIC_|OPENAI_|DEEPSEEK_|POSTGRES_)" .env | head -10
else
    echo "❌ .env не найден в корне"
fi

if [ -f ".env.example" ]; then
    echo "✅ .env.example найден"
else
    echo "❌ .env.example не найден"
fi
echo ""

# 6. Проверяем requirements.txt
echo "📦 PYTHON ЗАВИСИМОСТИ:"
echo "----------------------"
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt найден"
    echo "Основные зависимости:"
    head -10 requirements.txt
else
    echo "❌ requirements.txt не найден"
fi
echo ""

# 7. Проверяем запущенные процессы
echo "🔄 ЗАПУЩЕННЫЕ ПРОЦЕССЫ:"
echo "----------------------"
echo "Python процессы:"
ps aux | grep python | grep -v grep | head -5
echo ""
echo "Docker контейнеры:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -10
echo ""

# 8. Проверяем порты
echo "🌐 ЗАНЯТЫЕ ПОРТЫ:"
echo "----------------"
echo "Порт 8000 (Backend API):"
netstat -tulpn | grep :8000 || echo "Порт 8000 свободен"
echo ""
echo "Порт 5000 (Bot):"
netstat -tulpn | grep :5000 || echo "Порт 5000 свободен"
echo ""

# 9. Проверяем логи
echo "📋 ЛОГИ:"
echo "--------"
if [ -d "logs" ]; then
    echo "✅ Директория logs найдена"
    ls -la logs/
else
    echo "❌ Директория logs не найдена"
fi
echo ""

# 10. Проверяем API напрямую
echo "🔧 ПРОВЕРКА API:"
echo "---------------"
echo "Backend Health Check (прямое подключение):"
curl -s http://207.154.220.86:8000/health 2>/dev/null || echo "❌ Backend API недоступен"
echo ""

echo "Проверка API агентов:"
curl -s http://207.154.220.86:8000/api/agents/status 2>/dev/null || echo "❌ API agents недоступен"
echo ""

# 11. Проверяем nginx конфигурацию на сервере
echo "🌐 NGINX КОНФИГУРАЦИЯ:"
echo "---------------------"
if [ -d "/etc/nginx/sites-available" ]; then
    echo "Конфигурации сайтов:"
    ls /etc/nginx/sites-available/ | grep -E "(aisolar|backend)"
else
    echo "❌ Nginx sites-available не найден"
fi
echo ""

# 12. Проверяем базу данных
echo "🗄️  БАЗА ДАННЫХ:"
echo "----------------"
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL CLI доступен"
    # Проверяем подключение к БД (если настроено)
    if [ ! -z "$DATABASE_URL" ]; then
        echo "Проверка подключения к БД..."
        psql $DATABASE_URL -c "SELECT version();" 2>/dev/null | head -1 || echo "❌ Не удалось подключиться к БД"
    else
        echo "❌ DATABASE_URL не настроен"
    fi
else
    echo "❌ PostgreSQL CLI недоступен"
fi
echo ""

# 13. Проверяем системные ресурсы
echo "💻 СИСТЕМНЫЕ РЕСУРСЫ:"
echo "--------------------"
echo "CPU и Memory:"
top -bn1 | grep "Cpu\|Mem" | head -2
echo ""
echo "Дисковое пространство:"
df -h | grep -E "(/$|/var)"
echo ""

# 14. Создаем план исправления
echo "🎯 ПЛАН ИСПРАВЛЕНИЯ:"
echo "==================="
echo ""
echo "1. Настроить поддомен backend.aisolar.swapoil.de в nginx"
echo "2. Обновить DNS записи для backend поддомена"
echo "3. Исправить конфигурацию backend для работы на поддомене"
echo "4. Обновить frontend для подключения к backend.aisolar.swapoil.de"
echo "5. Настроить SSL сертификаты для поддомена"
echo ""

echo "✅ ПРОВЕРКА ЗАВЕРШЕНА!"
echo ""
echo "📋 Следующие команды для получения файлов:"
echo "cat docker-compose.yml"
echo "cat .env"
echo "cat requirements.txt"
echo "ls -la"
