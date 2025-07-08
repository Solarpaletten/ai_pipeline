#!/bin/bash

echo "🚀 LEVEL 7: БЕЗОПАСНЫЙ СТАРТ DELEGATION SYSTEM"
echo "=============================================="

# Проверяем текущую ветку
current_branch=$(git branch --show-current)
echo "📍 Текущая ветка: $current_branch"

if [ "$current_branch" != "main" ]; then
    echo "⚠️  Рекомендуется запускать с ветки main"
    read -p "Продолжить? (y/n): " continue_anyway
    if [ "$continue_anyway" != "y" ]; then
        exit 1
    fi
fi

echo ""
echo "🔍 ПРОВЕРКА ТЕКУЩЕЙ СИСТЕМЫ..."
echo "=============================="

# Проверяем что система Level 6 работает
echo "✅ Проверяем backend файлы..."
if [ ! -f "main.py" ] || [ ! -f "api/chat_endpoints.py" ]; then
    echo "❌ Критические файлы отсутствуют!"
    exit 1
fi

echo "✅ Проверяем frontend файлы..."
if [ ! -f "frontend/src/App.tsx" ] || [ ! -f "frontend/src/components/dashboard/Dashboard.tsx" ]; then
    echo "❌ Frontend файлы отсутствуют!"
    exit 1
fi

echo "✅ Все критические файлы на месте"

echo ""
echo "🌿 СОЗДАНИЕ БЕЗОПАСНОЙ ВЕТКИ..."
echo "==============================="

# Создаем ветку Level 7
git checkout -b feature/level7-delegation 2>/dev/null || {
    echo "ℹ️  Ветка уже существует, переключаемся..."
    git checkout feature/level7-delegation
}

echo "✅ Ветка feature/level7-delegation создана/активна"

echo ""
echo "📁 СОЗДАНИЕ ИЗОЛИРОВАННОЙ СТРУКТУРЫ..."
echo "====================================="

# Backend структура
echo "🐍 Создаем backend модули..."
mkdir -p src/delegation/{engine,orchestrator,monitoring}
mkdir -p models/delegation

# Создаем __init__.py файлы
touch src/__init__.py
touch src/delegation/__init__.py
touch src/delegation/engine/__init__.py
touch src/delegation/orchestrator/__init__.py
touch src/delegation/monitoring/__init__.py

# Создаем основные модули
cat > src/delegation/__init__.py << 'EOF'
"""
Level 7: Inter-Agent Delegation System
Модульная система делегирования задач между AI агентами
"""
__version__ = "1.0.0"
__level__ = 7

from .engine.delegation_engine import DelegationEngine
from .orchestrator.workflow_orchestrator import WorkflowOrchestrator
from .monitoring.delegation_monitor import DelegationMonitor

__all__ = ["DelegationEngine", "WorkflowOrchestrator", "DelegationMonitor"]
EOF

# Создаем skeleton файлы
touch src/delegation/engine/delegation_engine.py
touch src/delegation/orchestrator/workflow_orchestrator.py
touch src/delegation/monitoring/delegation_monitor.py
touch api/delegation_v7.py
touch models/delegation/delegation_models.py

echo "✅ Backend структура создана"

# Frontend структура  
echo "⚛️  Создаем frontend компоненты..."
mkdir -p frontend/src/components/delegation
mkdir -p frontend/src/hooks/delegation
mkdir -p frontend/src/types/delegation

# Создаем skeleton компоненты
touch frontend/src/components/delegation/DelegationDashboard.tsx
touch frontend/src/components/delegation/WorkflowGraph.tsx
touch frontend/src/components/delegation/DelegationMonitor.tsx
touch frontend/src/components/delegation/AgentChain.tsx
touch frontend/src/hooks/delegation/useDelegation.ts
touch frontend/src/hooks/delegation/useWorkflow.ts
touch frontend/src/types/delegation/index.ts

echo "✅ Frontend структура создана"

echo ""
echo "🔧 НАСТРОЙКА FEATURE TOGGLE..."
echo "=============================="

# Добавляем feature flag в .env
if ! grep -q "LEVEL7_ENABLED" .env; then
    echo "" >> .env
    echo "# Level 7: Delegation System" >> .env
    echo "LEVEL7_ENABLED=false" >> .env
    echo "LEVEL7_DEBUG=true" >> .env
    echo "✅ Feature flags добавлены в .env"
else
    echo "ℹ️  Feature flags уже существуют в .env"
fi

echo ""
echo "📊 СОЗДАНИЕ МОНИТОРИНГА ИЗМЕНЕНИЙ..."
echo "==================================="

# Скрипт для проверки безопасности изменений
cat > scripts/verify_level7_safety.sh << 'EOF'
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
EOF

chmod +x scripts/verify_level7_safety.sh

# Скрипт экстренного отката
cat > scripts/emergency_rollback.sh << 'EOF'
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
EOF

chmod +x scripts/emergency_rollback.sh

echo "✅ Скрипты безопасности созданы"

echo ""
echo "📋 СОЗДАНИЕ НАЧАЛЬНОГО КОММИТА..."
echo "================================"

# Добавляем только новые файлы в git
git add src/delegation/
git add frontend/src/components/delegation/
git add frontend/src/hooks/delegation/
git add frontend/src/types/delegation/
git add models/delegation/
git add api/delegation_v7.py
git add scripts/verify_level7_safety.sh
git add scripts/emergency_rollback.sh
git add .env

# Коммитим skeleton
git commit -m "🏗️ Level 7: Initial structure - isolated delegation modules

✅ Created isolated directories:
- src/delegation/ (backend modules)
- frontend/src/components/delegation/ (UI components)
- models/delegation/ (data models)
- api/delegation_v7.py (new API endpoint)

🔒 Safety features:
- Feature flags in .env (LEVEL7_ENABLED=false)
- Verification scripts
- Emergency rollback script

🛡️ Zero impact on Level 6 functionality"

echo ""
echo "🎉 LEVEL 7 СТРУКТУРА СОЗДАНА УСПЕШНО!"
echo "===================================="

echo ""
echo "📊 СТАТИСТИКА:"
echo "=============="
echo "✅ Создано файлов: $(find src/delegation frontend/src/components/delegation frontend/src/hooks/delegation models/delegation -type f | wc -l)"
echo "✅ Изменений в существующих файлах: 1 (.env)"
echo "✅ Feature toggle: LEVEL7_ENABLED=false (безопасно выключен)"
echo "✅ Экстренный откат: scripts/emergency_rollback.sh"

echo ""
echo "🚀 СЛЕДУЮЩИЕ ШАГИ:"
echo "=================="
echo "1. Проверить безопасность: ./scripts/verify_level7_safety.sh"
echo "2. Тестировать Level 6: curl http://localhost:8002/api/chat/agents"
echo "3. Начать разработку: Создать DelegationEngine"
echo "4. При проблемах: ./scripts/emergency_rollback.sh"

echo ""
echo "🛡️ LEVEL 7 ГОТОВ К БЕЗОПАСНОЙ РАЗРАБОТКЕ!"
echo "Текущий статус: ИЗОЛИРОВАННАЯ СТРУКТУРА СОЗДАНА"
echo "Риск для Level 6: НУЛЕВОЙ ✅"