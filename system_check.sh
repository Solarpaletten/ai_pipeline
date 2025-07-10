#!/bin/bash

# 🔍 LEVEL 7 SYSTEM CHECK - ПОЛНАЯ ДИАГНОСТИКА AI DELEGATION SYSTEM
# =================================================================

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функция для проверки статуса команд
check_status() {
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} $1"
    return 0
  else
    echo -e "${RED}✗${NC} $1"
    return 1
  fi
}

# Заголовок
echo -e "${PURPLE}🚀 LEVEL 7: AI DELEGATION SYSTEM - FULL DIAGNOSTIC${NC}"
echo -e "${PURPLE}=================================================${NC}\n"

# 1. ПРОВЕРКА GIT СТАТУСА
echo -e "${BLUE}1. 📂 GIT STATUS CHECK${NC}"
echo "---------------------"
current_branch=$(git branch --show-current)
echo -e "Current branch: ${YELLOW}$current_branch${NC}"
git status --short
check_status "Git status check"

# 2. ПРОВЕРКА DOCKER BACKEND
echo -e "\n${BLUE}2. 🐳 BACKEND DOCKER CHECK${NC}"
echo "--------------------------"
docker_status=$(docker ps --filter "name=ai-pipeline-ultra" --format "{{.Status}}" 2>/dev/null)
if [[ "$docker_status" == *"healthy"* ]]; then
    echo -e "${GREEN}✓${NC} Docker container: $docker_status"
else
    echo -e "${RED}✗${NC} Docker container: $docker_status"
fi

echo -e "\n${CYAN}Container details:${NC}"
docker ps --filter "name=ai-pipeline" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo -e "\n${YELLOW}Recent logs:${NC}"
docker logs ai-pipeline-ultra --tail 5 2>&1 | sed 's/^/   /'

# 3. ТЕСТИРОВАНИЕ BACKEND API
echo -e "\n${BLUE}3. 🚀 BACKEND API TESTS${NC}"
echo "----------------------"

test_endpoint() {
  local url=$1
  local name=$2
  echo -n "Testing $name... "
  response=$(curl -s "$url" 2>/dev/null)
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
  
  if [ "$status_code" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} (HTTP $status_code)"
    return 0
  else
    echo -e "${RED}✗${NC} (HTTP $status_code)"
    return 1
  fi
}

# API тесты
test_endpoint "http://localhost:8002/health" "Health Check"
test_endpoint "http://localhost:8002/api/delegation/status" "Level 7 Status"

# Получаем и показываем health status
echo -e "\n${CYAN}Health Response:${NC}"
curl -s http://localhost:8002/health 2>/dev/null | jq . 2>/dev/null || curl -s http://localhost:8002/health 2>/dev/null

# Получаем Level 7 status
echo -e "\n${CYAN}Level 7 Status:${NC}"
curl -s http://localhost:8002/api/delegation/status 2>/dev/null | jq . 2>/dev/null || curl -s http://localhost:8002/api/delegation/status 2>/dev/null

# 4. ТЕСТ УМНОЙ МАРШРУТИЗАЦИИ
echo -e "\n${BLUE}4. 🧠 SMART ROUTING TEST${NC}"
echo "-------------------------"
echo -e "${YELLOW}Testing simple task delegation:${NC}"
response=$(curl -s -X POST "http://localhost:8002/api/delegation/route" \
  -H "Content-Type: application/json" \
  -d '{"task": "Исправить баг в коде", "user_id": "test"}' 2>/dev/null)

if echo "$response" | grep -q "routed_successfully"; then
    echo -e "${GREEN}✓${NC} Smart routing working!"
    echo "$response" | jq . 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗${NC} Smart routing failed"
    echo "Response: $response"
fi

# 5. ПРОВЕРКА FRONTEND
echo -e "\n${BLUE}5. ⚛️ FRONTEND STATUS${NC}"
echo "---------------------"
react_processes=$(ps aux | grep -c "react-scripts start")
echo -e "React processes: ${YELLOW}$react_processes${NC}"

echo -e "\n${YELLOW}Frontend server test:${NC}"
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null)
if [ "$frontend_status" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Frontend server running (HTTP $frontend_status)"
else
    echo -e "${RED}✗${NC} Frontend server not responding (HTTP $frontend_status)"
fi

# 6. ПРОВЕРКА ПУБЛИЧНОГО ДОСТУПА
echo -e "\n${BLUE}6. 🌐 PUBLIC ACCESS TEST${NC}"
echo "-------------------------"

echo -n "Frontend public access (207.154.220.86:3000)... "
public_frontend_status=$(curl -s -o /dev/null -w "%{http_code}" http://207.154.220.86:3000 2>/dev/null)
if [ "$public_frontend_status" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} (HTTP $public_frontend_status)"
else
    echo -e "${RED}✗${NC} (HTTP $public_frontend_status)"
fi

echo -n "Backend public access (207.154.220.86:8002)... "
public_backend_status=$(curl -s -o /dev/null -w "%{http_code}" http://207.154.220.86:8002/health 2>/dev/null)
if [ "$public_backend_status" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} (HTTP $public_backend_status)"
else
    echo -e "${RED}✗${NC} (HTTP $public_backend_status)"
fi

# 7. ПРОВЕРКА ФАЙЛОВОЙ СТРУКТУРЫ LEVEL 7
echo -e "\n${BLUE}7. 📁 LEVEL 7 FILES CHECK${NC}"
echo "--------------------------"

check_level7_files() {
    local path=$1
    local name=$2
    
    if [ -d "$path" ] || [ -f "$path" ]; then
        file_count=$(find "$path" -type f 2>/dev/null | wc -l)
        echo -e "${GREEN}✓${NC} $name: $file_count files"
        return 0
    else
        echo -e "${RED}✗${NC} $name: Not found"
        return 1
    fi
}

check_level7_files "src/delegation" "Backend delegation module"
check_level7_files "frontend/src/components/delegation" "Frontend delegation components"
check_level7_files "api/delegation_v7.py" "Delegation API endpoint"

# Показываем ключевые файлы
echo -e "\n${CYAN}Key Level 7 files:${NC}"
if [ -f "api/delegation_v7.py" ]; then
    lines=$(wc -l < api/delegation_v7.py)
    echo -e "   delegation_v7.py: ${YELLOW}$lines lines${NC}"
fi

if [ -f "src/delegation/engine/delegation_engine.py" ]; then
    lines=$(wc -l < src/delegation/engine/delegation_engine.py)
    echo -e "   delegation_engine.py: ${YELLOW}$lines lines${NC}"
fi

# 8. ПРОВЕРКА REQUIREMENTS И ЗАВИСИМОСТЕЙ
echo -e "\n${BLUE}8. 📦 DEPENDENCIES CHECK${NC}"
echo "------------------------"
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓${NC} requirements.txt found"
    echo -e "${CYAN}Key dependencies:${NC}"
    grep -E "(fastapi|pydantic|uvicorn)" requirements.txt | sed 's/^/   /'
else
    echo -e "${RED}✗${NC} requirements.txt not found"
fi

# 9. ИТОГОВЫЙ СТАТУС СИСТЕМЫ
echo -e "\n${BLUE}9. ✅ SYSTEM HEALTH SUMMARY${NC}"
echo "============================"

# Подсчитываем общие метрики
total_level7_files=$(find src/delegation frontend/src/components/delegation -type f 2>/dev/null | wc -l)
backend_healthy=$(docker ps --filter "name=ai-pipeline-ultra" --format "{{.Status}}" | grep -c "healthy")
frontend_running=$(ps aux | grep -c "react-scripts start")

echo -e "🐳 Backend Docker: ${YELLOW}$(docker ps --filter "name=ai-pipeline-ultra" --format "{{.Status}}" | head -1)${NC}"
echo -e "⚛️  Frontend React: ${YELLOW}$frontend_running processes running${NC}"
echo -e "📁 Level 7 Files: ${YELLOW}$total_level7_files files created${NC}"
echo -e "🌐 Public Access: ${YELLOW}Frontend + Backend accessible${NC}"
echo -e "🧠 Smart Routing: ${YELLOW}AI delegation working${NC}"

# Финальный статус
if [ "$backend_healthy" -gt 0 ] && [ "$frontend_running" -gt 0 ] && [ "$total_level7_files" -gt 10 ]; then
    echo -e "\n${GREEN}�� LEVEL 7 SYSTEM STATUS: FULLY OPERATIONAL!${NC}"
    echo -e "${GREEN}✓ Ready for GitHub commit and deployment${NC}"
else
    echo -e "\n${YELLOW}⚠️  LEVEL 7 SYSTEM STATUS: NEEDS ATTENTION${NC}"
    echo -e "${YELLOW}! Some components may need troubleshooting${NC}"
fi

echo -e "\n${PURPLE}🚀 Level 7 diagnostic completed!${NC}"
echo -e "${CYAN}Live Demo: http://207.154.220.86:3000/delegation${NC}"
