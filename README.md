# AI Pipeline
Проект для делегирования задач между Claude и DeepSeek.

## Запуск
```bash
docker-compose -f config/docker-compose.yml up -d


# Telegram Bot
TELEGRAM_BOT_TOKEN=7226462262:AAESuhHmehkme_oPwhafMz_z994nBBZDi38

# AI APIs
ANTHROPIC_API_KEY=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
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_MAX_TOKENS=4000

OPENAI_API_KEY=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
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

DEEPSEEK_API_KEY=sk-85fc8273963a43eb9ec4644066132def
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-coder

# Database
POSTGRES_DB=aisolar
POSTGRES_USER=aisolar
POSTGRES_PASSWORD=password_here
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql://aisolar:password_here@postgres:5432/aisolar

# Environment
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development

PORT=8000
HOST=0.0.0.0