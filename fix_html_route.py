# Добавляем HTML route в web_server.py
import re

# Читаем текущий web_server.py
with open('web_server.py', 'r') as f:
    content = f.read()

# Заменяем root route на HTML версию
html_route = '''
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Главная страница Dashboard"""
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AI Pipeline Level 3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .container { 
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
            border-radius: 20px; padding: 40px; box-shadow: 0 25px 45px rgba(0,0,0,0.1);
            max-width: 800px; width: 90%;
        }
        h1 { color: #2d3748; text-align: center; margin-bottom: 10px; font-size: 2.5rem; font-weight: 700; }
        .subtitle { text-align: center; color: #718096; margin-bottom: 40px; font-size: 1.1rem; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .status-card { background: white; border-radius: 15px; padding: 25px; text-align: center; 
                      box-shadow: 0 10px 25px rgba(0,0,0,0.08); border: 2px solid #e2e8f0; 
                      transition: all 0.3s ease; }
        .status-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.12); }
        .status-icon { font-size: 3rem; margin-bottom: 15px; }
        .status-title { font-weight: 600; color: #2d3748; margin-bottom: 8px; }
        .status-value { color: #48bb78; font-weight: 700; font-size: 1.1rem; }
        .nav-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .nav-button { display: block; background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                     color: white; text-decoration: none; padding: 20px; border-radius: 12px;
                     text-align: center; font-weight: 600; transition: all 0.3s ease;
                     box-shadow: 0 8px 20px rgba(66, 153, 225, 0.3); }
        .nav-button:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(66, 153, 225, 0.4);
                           background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%); }
        .nav-button.secondary { background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                               box-shadow: 0 8px 20px rgba(72, 187, 120, 0.3); }
        .nav-button.secondary:hover { background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
                                     box-shadow: 0 12px 30px rgba(72, 187, 120, 0.4); }
        .footer { text-align: center; margin-top: 30px; color: #718096; font-size: 0.9rem; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .pulse { animation: pulse 2s infinite; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AI Pipeline</h1>
        <p class="subtitle">Level 3 Production Dashboard</p>
        
        <div class="status-grid">
            <div class="status-card">
                <div class="status-icon">🎛️</div>
                <div class="status-title">Dashka Bot</div>
                <div class="status-value pulse">Online</div>
            </div>
            <div class="status-card">
                <div class="status-icon">🧠</div>
                <div class="status-title">Claude AI</div>
                <div class="status-value pulse">Online</div>
            </div>
            <div class="status-card">
                <div class="status-icon">💻</div>
                <div class="status-title">DeepSeek AI</div>
                <div class="status-value pulse">Online</div>
            </div>
        </div>

        <div class="nav-grid">
            <a href="/api/agents/status" class="nav-button">📊 Статус агентов</a>
            <a href="/docs" class="nav-button">📚 API документация</a>
            <a href="/health" class="nav-button secondary">🏥 Health Check</a>
            <a href="/api/delegations/recent" class="nav-button secondary">📋 Последние задачи</a>
        </div>

        <div class="footer">
            <p>✅ All systems operational • Level 3 Backend API • Production Ready</p>
        </div>
    </div>

    <script>
        async function checkStatus() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                console.log('✅ Backend status:', data);
            } catch (error) {
                console.log('❌ Backend error:', error);
            }
        }
        checkStatus();
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)
'''

# Заменяем старый root route
pattern = r'@app\.get\("/"\).*?async def read_root.*?return.*?\n'
new_content = re.sub(pattern, html_route, content, flags=re.DOTALL)

# Записываем обновленный файл
with open('web_server.py', 'w') as f:
    f.write(new_content)

print("✅ HTML route добавлен в web_server.py")
