# 🚀 Quick Start Guide

## One-Command Setup

```bash
python setup.py
```

This script will:

- ✅ Install all dependencies
- ✅ Create .env file from template
- ✅ Run database migrations
- ✅ Collect static files
- ✅ Optionally create superuser
- ✅ Optionally seed sample data

## Manual Setup (if you prefer)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
cp .env.example .env
# Edit .env with your actual settings
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
python manage.py collectstatic
```

### 6. Seed Sample Data (Optional)

```bash
python manage.py seed_products
```

### 7. Run Server

```bash
python manage.py runserver
```

## 🌐 Access Points

- **Frontend**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Admin Dashboard**: http://127.0.0.1:8000/admin-panel/

## 📱 Features Available

### Customer Features

- ✅ User registration and login
- ✅ Product browsing and search
- ✅ Shopping cart management
- ✅ Wishlist functionality
- ✅ Order placement and tracking
- ✅ Profile management

### Admin Features

- ✅ Product management (CRUD)
- ✅ Category management
- ✅ Order management
- ✅ User management
- ✅ Dashboard with statistics
- ✅ Export functionality

### Payment Features

- ✅ Stripe integration
- ✅ Secure payment processing
- ✅ Order status tracking

## 🔧 Configuration

### Environment Variables (.env)

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=pk_test_your-key
STRIPE_SECRET_KEY=sk_test_your-key
STRIPE_WEBHOOK_SECRET=whsec_your-secret
```

## 📁 Project Structure

```
django-ec/
├── accounts/          # User authentication
├── admin/            # Custom admin panel
├── cart/             # Shopping cart
├── catalog/          # Products & categories
├── orders/           # Order management
├── payments/         # Stripe payments
├── wishlist/         # Wishlist functionality
├── templates/        # HTML templates
├── static/           # CSS & JS files
├── media/            # User uploads
├── ecsite/           # Django settings
├── manage.py         # Django management
├── requirements.txt  # Dependencies
├── .env.example      # Environment template
└── setup.py          # Setup script
```

## 🎯 Next Steps

1. **Configure Stripe**: Get your API keys from https://dashboard.stripe.com
2. **Customize Design**: Modify templates and CSS
3. **Add Products**: Use admin panel to add products
4. **Test Payments**: Use Stripe test mode
5. **Deploy**: Follow deployment guide in README.md

## 🆘 Troubleshooting

### Django Not Found

```bash
# Activate virtual environment first
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### Migration Issues

```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Static Files Not Loading

```bash
python manage.py collectstatic --clear --noinput
```

### Stripe Issues

- Verify API keys in .env file
- Check webhook endpoint configuration
- Use test mode for development

## 📞 Support

- Check README.md for detailed documentation
- Review Django documentation: https://docs.djangoproject.com/
- Stripe integration docs: https://stripe.com/docs/
