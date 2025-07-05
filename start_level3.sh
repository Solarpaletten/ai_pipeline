#!/bin/bash

echo "🚀 Запуск AI Pipeline Level 3"

# Проверяем зависимости
echo "📦 Проверяем зависимости..."
pip install -r requirements.txt

# Запускаем веб-сервер
echo "🌐 Запускаем веб-сервер на порту 8000..."
python web_server.py &

echo "✅ Level 3 запущен!"
echo "📊 Dashboard: http://localhost:8000/static_dashboard.html"
echo "📡 API: http://localhost:8000/docs"
echo "🔍 Health: http://localhost:8000/health"
