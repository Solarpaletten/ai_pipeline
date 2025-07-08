#!/bin/bash

echo "=========================="
echo "📁 Project Structure Analysis"
echo "=========================="

# Основные файлы
echo -e "\n🏠 ROOT FILES:"
ls -la | grep -vE "(node_modules|venv|__pycache__|.git|.vscode|.idea)" | awk '{print $9}' | grep -v "^$"

# Backend структура
echo -e "\n🐍 BACKEND STRUCTURE:"
find . -maxdepth 3 -type d \( -name "api" -o -name "core" -o -name "services" -o -name "models" \) -exec ls -ld {} \; 2>/dev/null
find . -maxdepth 3 -type f \( -name "*.py" ! -path "./venv/*" ! -path "./frontend/node_modules/*" \) | head -15

# Frontend структура
echo -e "\n⚛️ FRONTEND STRUCTURE:"
if [ -d "frontend" ]; then
    find frontend -maxdepth 3 -type d \( -name "src" -o -name "public" -o -name "components" \) -exec ls -ld {} \; 2>/dev/null
    find frontend/src -maxdepth 2 -type f \( -name "*.tsx" -o -name "*.ts" \) | head -10
else
    echo "Frontend directory not found"
fi

# Docker файлы
echo -e "\n🐳 DOCKER FILES:"
ls -la Dockerfile* docker-compose* 2>/dev/null

# Критические файлы
echo -e "\n🔍 CRITICAL FILES:"
ls -la main.py api/chat_endpoints.py services/ai_integrations.py 2>/dev/null

# Статистика
echo -e "\n📊 STATISTICS:"
echo "Python files: $(find . -name "*.py" ! -path "./venv/*" ! -path "./frontend/node_modules/*" | wc -l)"
echo "TypeScript files: $(find . -name "*.ts*" ! -path "./node_modules/*" ! -path "./frontend/node_modules/*" | wc -l)"
echo "Total size: $(du -sh . | cut -f1)"

echo -e "\n✅ Analysis complete!"