#!/bin/bash
echo "🔍 ПРОВЕРКА БЕЗОПАСНОСТИ LEVEL 7"
echo "==============================="

echo "📁 Новые файлы (должны быть только в изолированных папках):"
git status --porcelain | grep "^??" | while read line; do
    file=$(echo $line | cut -d' ' -f2-)
    if [[ $file =~ ^src/delegation/ ]] || [[ $file =~ ^frontend/src/components/delegation/ ]] || [[ $file =~ ^frontend/src/hooks/delegation/ ]] || [[ $file =~ ^frontend/src/types/delegation/ ]] || [[ $file =~ ^models/delegation/ ]] || [[ $file =~ ^api/delegation_v7.py ]] || [[ $file =~ ^scripts/ ]]; then
        echo "✅ $file (безопасно)"
    else
        echo "⚠️  $file (ПРОВЕРИТЬ!)"
    fi
done

echo ""
echo "📝 Измененные файлы (должно быть минимум):"
git status --porcelain | grep "^.M" | while read line; do
    file=$(echo $line | cut -d' ' -f2-)
    if [[ $file == "main.py" ]] || [[ $file == "frontend/src/App.tsx" ]] || [[ $file == ".env" ]]; then
        echo "✅ $file (ожидаемое изменение)"
    else
        echo "⚠️  $file (ВНИМАНИЕ: неожиданное изменение!)"
    fi
done

echo ""
echo "🧪 Рекомендация: Запустите тесты Level 6 перед продолжением"
echo "pytest tests/ || curl http://localhost:8002/api/chat/agents"
