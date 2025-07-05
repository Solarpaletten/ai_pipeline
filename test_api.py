#!/usr/bin/env python3
import urllib.request
import json

def test_endpoint(url, name):
    try:
        print(f"🔍 Тестируем {name}...")
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        print(f"✅ {name}:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print()
        return True
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

print("🚀 Тестирование AI Pipeline Backend API Level 3\n")
test_endpoint('http://localhost:8000/health', 'Health Check')
test_endpoint('http://localhost:8000/api/agents/status', 'Agents Status')
test_endpoint('http://localhost:8000/', 'Root Endpoint')

print("📊 Доступные URLs для браузера:")
print("   Dashboard: http://localhost:8000/static_dashboard.html")
print("   API Docs:  http://localhost:8000/docs")
