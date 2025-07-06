#!/bin/bash

echo "🔍 Проверка интеграции AI Pipeline Dashboard с Backend"
echo ""

# Проверяем frontend
echo "📱 Frontend Health Check:"
curl -s http://localhost/health || echo "❌ Frontend недоступен"
echo ""

# Проверяем backend через proxy
echo "🔧 Backend Health Check (через proxy):"
curl -s http://localhost/backend-health || echo "❌ Backend недоступен через proxy"
echo ""

# Проверяем прямое подключение к backend
echo "🔧 Backend Direct Check:"
curl -s http://207.154.220.86:8000/health || echo "❌ Backend недоступен напрямую"
echo ""

# Проверяем API endpoint
echo "📡 API Check:"
curl -s http://localhost/api/agents/status || echo "❌ API agents недоступен"
echo ""

# Проверяем Docker контейнеры
echo "🐳 Docker Status:"
docker-compose -f docker-compose.production.yml ps
echo ""

echo "✅ Проверка завершена!"
