#!/usr/bin/env python3
"""
Django E-Commerce Site Setup Script
This script helps set up the entire project from scratch.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Django E-Commerce Site Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Step 2: Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("\n🔧 Creating .env file...")
        try:
            with open(".env.example", "r") as f:
                env_content = f.read()
            
            with open(".env", "w") as f:
                f.write(env_content)
            print("✅ .env file created from .env.example")
            print("⚠️  Please edit .env file with your actual settings before running the server")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
    
    # Step 3: Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        sys.exit(1)
    
    # Step 4: Create superuser (optional)
    create_superuser = input("\n📝 Do you want to create a superuser? (y/n): ").lower()
    if create_superuser == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Step 5: Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    # Step 6: Seed sample data (optional)
    seed_data = input("\n📝 Do you want to seed sample data? (y/n): ").lower()
    if seed_data == 'y':
        run_command("python manage.py seed_products", "Seeding sample products")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your actual settings (Stripe keys, etc.)")
    print("2. Run 'python manage.py runserver' to start the development server")
    print("3. Visit http://127.0.0.1:8000/ to see your site")
    print("4. Visit http://127.0.0.1:8000/admin/ to access the admin panel")

if __name__ == "__main__":
    main()
