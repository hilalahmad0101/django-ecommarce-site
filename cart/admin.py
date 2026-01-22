from django.contrib import admin
from .cart import Cart

# Cart doesn't have persistent models, but we can add admin for any cart-related models if needed
# For now, cart functionality is handled through the session-based Cart class
