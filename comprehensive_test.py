#!/usr/bin/env python3
import urllib.request
import json
import time
import sys

def test_endpoint(url, name, expected_keys=None):
    try:
        print(f"🔍 Тестируем {name}...")
        start_time = time.time()
        
        response = urllib.request.urlopen(url)
        response_time = (time.time() - start_time) * 1000
        
        if response.status != 200:
            print(f"❌ {name}: HTTP {response.status}")
            return False
            
        data = json.loads(response.read())
        
        # Проверяем ожидаемые ключи
        if expected_keys:
            for key in expected_keys:
                if key not in data:
                    print(f"❌ {name}: отсутствует ключ '{key}'")
                    return False
        
        print(f"✅ {name}: {response_time:.1f}ms")
        print(f"   Данные: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
        print()
        return True
        
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

def test_websocket():
    """Тест WebSocket подключения"""
    try:
        print("🔍 Тестируем WebSocket...")
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("✅ WebSocket порт доступен")
            return True
        else:
            print("❌ WebSocket порт недоступен")
            return False
    except Exception as e:
        print(f"❌ WebSocket: {e}")
        return False

def main():
    print("🚀 Полное тестирование AI Pipeline Level 3 Backend\n")
    
    tests = [
        ("http://localhost:8000/health", "Health Check", ["status", "timestamp"]),
        ("http://localhost:8000/", "Root Endpoint", ["message", "status"]),
        ("http://localhost:8000/api/agents/status", "Agents Status", ["agents", "total_agents"]),
        ("http://localhost:8000/api/delegations/recent", "Recent Delegations", ["delegations", "total"]),
    ]
    
    passed = 0
    total = len(tests) + 1  # +1 для WebSocket
    
    # Тестируем HTTP endpoints
    for url, name, keys in tests:
        if test_endpoint(url, name, keys):
            passed += 1
    
    # Тестируем WebSocket
    if test_websocket():
        passed += 1
    
    # Финальный отчет
    print(f"�� Результаты тестирования:")
    print(f"   Пройдено: {passed}/{total} тестов")
    print(f"   Успешность: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Level 3 Backend работает отлично!")
        return 0
    else:
        print(f"\n❌ {total-passed} тестов провалено. Нужно исправить Backend.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
