# AI Pipeline Level 3 - Backend API

## Новые компоненты

### Web Server
- `web_server.py` - FastAPI сервер с WebSocket
- `api/` - API endpoints
- `services/` - Сервисы мониторинга
- `middleware/` - HTTP middleware

### Endpoints
- `GET /` - Главная страница
- `GET /api/agents/status` - Статус агентов
- `GET /api/delegations/recent` - Последние делегирования
- `POST /api/delegations/log` - Логирование
- `WS /ws/dashboard` - WebSocket для real-time

### Запуск
```bash
./start_level3.sh
```

### Тестирование
- Dashboard: http://localhost:8000/static_dashboard.html
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
