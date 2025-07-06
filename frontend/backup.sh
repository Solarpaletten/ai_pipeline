#!/bin/bash

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup in $BACKUP_DIR"

# Backup configuration
cp -r nginx "$BACKUP_DIR/"
cp docker-compose.production.yml "$BACKUP_DIR/"
cp Dockerfile.production "$BACKUP_DIR/"
cp .env "$BACKUP_DIR/"

# Backup build
if [ -d "build" ]; then
    cp -r build "$BACKUP_DIR/"
fi

echo "✅ Backup created: $BACKUP_DIR"
