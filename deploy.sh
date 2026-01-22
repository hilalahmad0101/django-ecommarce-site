#!/bin/bash

# Django E-Commerce Deployment Script
# This script prepares the project for production deployment

echo "🚀 Django E-Commerce Deployment Setup"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

# Install production dependencies
echo "📦 Installing production dependencies..."
pip install -r requirements.txt
pip install gunicorn psycopg2-binary whitenoise

# Create production environment file
if [ ! -f ".env" ]; then
    echo "🔧 Creating production .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with production settings"
fi

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if needed
echo "👤 Creating superuser (optional)..."
read -p "Do you want to create a superuser? (y/n): " create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Seed sample data in development
if [ "$DEBUG" = "True" ]; then
    echo "🌱 Seeding sample data..."
    python manage.py seed_products
fi

echo "✅ Deployment setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your production database in .env"
echo "2. Set DEBUG=False in .env"
echo "3. Configure your web server (Nginx + Gunicorn)"
echo "4. Set up environment variables"
echo "5. Configure SSL certificate"
echo ""
echo "🔧 Gunicorn command example:"
echo "gunicorn ecsite.wsgi:application --bind 0.0.0.0:8000"
