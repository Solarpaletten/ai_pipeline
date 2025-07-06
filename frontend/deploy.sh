#!/bin/bash

set -e

echo "🚀 Deploying AI Pipeline Dashboard to aisolar.swapoil.de"
echo ""

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Run this script from the frontend directory"
    exit 1
fi

# Create logs directory
mkdir -p logs/nginx

echo "📦 Building production version..."
npm run build

echo "🐳 Stopping existing containers..."
docker-compose -f docker-compose.production.yml down

echo "🔨 Building new Docker image..."
docker-compose -f docker-compose.production.yml build --no-cache

echo "🚀 Starting services..."
docker-compose -f docker-compose.production.yml up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "📊 Service status:"
docker-compose -f docker-compose.production.yml ps

echo ""
echo "✅ Dashboard deployed successfully!"
echo ""
echo "🌐 Frontend URL: https://aisolar.swapoil.de"
echo "🔧 Backend URL: https://backend.aisolar.swapoil.de"
echo "📊 Health check: https://aisolar.swapoil.de/health"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose -f docker-compose.production.yml logs -f    # View logs"
echo "  docker-compose -f docker-compose.production.yml restart    # Restart services"
echo "  docker-compose -f docker-compose.production.yml down       # Stop services"
