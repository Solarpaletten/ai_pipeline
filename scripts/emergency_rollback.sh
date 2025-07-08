#!/bin/bash
echo "🚨 ЭКСТРЕННЫЙ ОТКАТ LEVEL 7"
echo "=========================="

echo "🔄 Возврат к безопасному состоянию..."

# Удаляем новые файлы
rm -rf src/delegation/
rm -rf frontend/src/components/delegation/
rm -rf frontend/src/hooks/delegation/
rm -rf frontend/src/types/delegation/
rm -rf models/delegation/
rm -f api/delegation_v7.py

# Восстанавливаем оригинальные файлы
git checkout HEAD -- main.py 2>/dev/null || echo "main.py не был изменен"
git checkout HEAD -- frontend/src/App.tsx 2>/dev/null || echo "App.tsx не был изменен"
git checkout HEAD -- .env 2>/dev/null || echo ".env восстановлен"

echo "✅ Откат завершен. Система вернулась к состоянию Level 6"
echo "🧪 Рекомендуется проверить работоспособность системы"
