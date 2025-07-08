# Dockerfile.ultra-minimal - Максимально компактный образ
FROM python:3.11-alpine

# Устанавливаем только критически важные пакеты
RUN apk add --no-cache gcc musl-dev curl

# Создаем пользователя
RUN adduser -D -s /bin/sh app

WORKDIR /app

# Копируем только requirements
COPY requirements.txt .

# Устанавливаем зависимости без кеша
RUN pip install --no-cache-dir --no-deps -r requirements.txt \
    && rm -rf /root/.cache

# Копируем только нужные файлы
COPY main.py .
COPY api/ ./api/
COPY core/ ./core/
COPY .env .

# Создаем директории
RUN mkdir -p logs static && chown -R app:app /app

USER app

EXPOSE 8002

# Минимальный healthcheck
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s \
    CMD curl -f http://localhost:8002/health || exit 1

CMD ["python", "main.py"]