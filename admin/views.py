from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from orders.models import Order
from catalog.models import Product, Category

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    
    recent_orders = Order.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_categories': total_categories,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/admin_dashboard.html', context)
