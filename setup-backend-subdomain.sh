#!/bin/bash

# 🌐 Настройка backend.aisolar.swapoil.de

echo "🌐 НАСТРОЙКА BACKEND ПОДДОМЕНА"
echo "==============================="
echo ""

# 1. Создаем nginx конфигурацию для backend поддомена
echo "📝 Создаем nginx конфигурацию для backend.aisolar.swapoil.de..."

sudo tee /etc/nginx/sites-available/backend.aisolar.swapoil.de << 'EOF'
server {
    listen 80;
    server_name backend.aisolar.swapoil.de;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name backend.aisolar.swapoil.de;
    
    # SSL настройки (обновите пути к вашим сертификатам)
    ssl_certificate /etc/ssl/certs/aisolar.crt;
    ssl_certificate_key /etc/ssl/private/aisolar.key;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # CORS headers для API
    add_header Access-Control-Allow-Origin "https://aisolar.swapoil.de" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
    add_header Access-Control-Allow-Credentials true always;
    
    # Proxy to backend API на порту 8000
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # CORS для OPTIONS requests
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin 'https://aisolar.swapoil.de';
            add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS';
            add_header Access-Control-Allow-Headers 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header Access-Control-Allow-Credentials true;
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain; charset=utf-8';
            add_header Content-Length 0;
            return 204;
        }
    }
    
    # Специальная настройка для WebSocket
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeout settings
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_connect_timeout 60s;
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        access_log off;
    }
}
EOF

echo "✅ Nginx конфигурация создана"

# 2. Активируем сайт
echo "🔗 Активируем сайт..."
sudo ln -sf /etc/nginx/sites-available/backend.aisolar.swapoil.de /etc/nginx/sites-enabled/

# 3. Проверяем конфигурацию nginx
echo "🔧 Проверяем конфигурацию nginx..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx конфигурация корректна"
    
    # 4. Перезагружаем nginx
    echo "🔄 Перезагружаем nginx..."
    sudo systemctl reload nginx
    echo "✅ Nginx перезагружен"
else
    echo "❌ Ошибка в конфигурации nginx"
    exit 1
fi

# 5. Проверяем статус nginx
echo "📊 Проверяем статус nginx..."
sudo systemctl status nginx --no-pager -l

# 6. Создаем скрипт проверки backend поддомена
cat > check-backend-subdomain.sh << 'EOF'
#!/bin/bash

echo "🔍 Проверка backend.aisolar.swapoil.de"
echo ""

echo "🌐 DNS проверка:"
nslookup backend.aisolar.swapoil.de || echo "❌ DNS не настроен"
echo ""

echo "🔧 HTTP проверка:"
curl -I http://backend.aisolar.swapoil.de/health 2>/dev/null || echo "❌ HTTP недоступен"
echo ""

echo "🔒 HTTPS проверка:"
curl -I https://backend.aisolar.swapoil.de/health 2>/dev/null || echo "❌ HTTPS недоступен"
echo ""

echo "📡 API проверка:"
curl -s https://backend.aisolar.swapoil.de/api/agents/status | head -3 || echo "❌ API недоступен"
echo ""

echo "🐳 Local backend проверка:"
curl -s http://127.0.0.1:8000/health || echo "❌ Local backend не работает"
echo ""
EOF

chmod +x check-backend-subdomain.sh

# 7. Обновляем frontend конфигурацию
echo "📝 Обновляем frontend .env..."
if [ -f "/var/www/ai_pipeline/frontend/.env" ]; then
    cat > /var/www/ai_pipeline/frontend/.env << 'EOF'
# Frontend Configuration для backend поддомена
REACT_APP_API_URL=https://backend.aisolar.swapoil.de/api
REACT_APP_WS_URL=wss://backend.aisolar.swapoil.de/ws/dashboard
GENERATE_SOURCEMAP=false
PORT=3000

# Production mode
REACT_APP_ENV=production
REACT_APP_DEBUG=false
EOF
    echo "✅ Frontend .env обновлен"
else
    echo "❌ Frontend .env не найден"
fi

echo ""
echo "🎯 НАСТРОЙКА ЗАВЕРШЕНА!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Настроить DNS запись для backend.aisolar.swapoil.de → 207.154.220.86"
echo "2. Запустить backend API на порту 8000"
echo "3. Проверить: ./check-backend-subdomain.sh"
echo "4. Пересобрать frontend с новой конфигурацией"
echo ""
echo "🌐 URL для проверки:"
echo "  Backend API: https://backend.aisolar.swapoil.de"
echo "  Health: https://backend.aisolar.swapoil.de/health"
echo "  API: https://backend.aisolar.swapoil.de/api/agents/status"
