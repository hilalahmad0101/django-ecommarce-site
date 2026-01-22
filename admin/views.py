from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from orders.models import Order, OrderItem
from catalog.models import Product, Category
from accounts.models import Profile
from .models import FAQ, ProductStats, CategoryStats, UserStats
from .forms import ProductForm, CategoryForm, FAQForm
import csv
import io
from datetime import datetime, timedelta

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get statistics
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # Additional stats
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    pending_orders = Order.objects.filter(status='pending').count()
    active_users = User.objects.filter(is_active=True).count()
    new_users_today = User.objects.filter(date_joined__date=timezone.now().date()).count()
    users_with_orders = User.objects.annotate(order_count=Count('order')).filter(order_count__gt=0).count()
    
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_categories': total_categories,
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'active_users': active_users,
        'new_users_today': new_users_today,
        'users_with_orders': users_with_orders,
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def product_list(request):
    products = Product.objects.select_related('category').all()
    
    # Search and filtering
    search = request.GET.get('search')
    category_id = request.GET.get('category')
    available = request.GET.get('available')
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if available:
        products = products.filter(available=(available == 'true'))
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = Category.objects.all()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'admin/product_list.html', context)

@login_required
@user_passes_test(is_admin)
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create stats
    stats, created = ProductStats.objects.get_or_create(product=product)
    
    # Get recent orders containing this product
    recent_orders = OrderItem.objects.filter(
        product=product
    ).select_related('order').order_by('-order__created_at')[:10]
    
    context = {
        'product': product,
        'stats': stats,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/product_detail.html', context)

@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            ProductStats.objects.create(product=product)
            messages.success(request, 'Product created successfully!')
            return redirect('admin:product_detail', product.id)
    else:
        form = ProductForm()
    
    return render(request, 'admin/product_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin:product_detail', product.id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/product_form.html', {'form': form, 'product': product})

@login_required
@user_passes_test(is_admin)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('admin:product_list')
    
    return render(request, 'admin/product_confirm_delete.html', {'product': product})

@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.annotate(product_count=Count('product'))
    
    # Stats
    total_products = Product.objects.count()
    avg_products_per_category = categories.aggregate(avg=Avg('product_count'))['avg'] or 0
    empty_categories = categories.filter(product_count=0).count()
    
    context = {
        'categories': categories,
        'total_products': total_products,
        'avg_products_per_category': round(avg_products_per_category, 1),
        'empty_categories': empty_categories,
    }
    return render(request, 'admin/category_list.html', context)

@login_required
@user_passes_test(is_admin)
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # Get or create stats
    stats, created = CategoryStats.objects.get_or_create(category=category)
    
    # Get products in this category
    products = category.product.all()
    
    context = {
        'category': category,
        'stats': stats,
        'products': products,
    }
    return render(request, 'admin/category_detail.html', context)

@login_required
@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            CategoryStats.objects.create(category=category)
            messages.success(request, 'Category created successfully!')
            return redirect('admin:category_detail', category.id)
    else:
        form = CategoryForm()
    
    return render(request, 'admin/category_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin:category_detail', category.id)
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/category_form.html', {'form': form, 'category': category})

@login_required
@user_passes_test(is_admin)
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('admin:category_list')
    
    return render(request, 'admin/category_confirm_delete.html', {'category': category})

@login_required
@user_passes_test(is_admin)
def order_list(request):
    orders = Order.objects.select_related('user').prefetch_related('items')
    
    # Filtering
    search = request.GET.get('search')
    status = request.GET.get('status')
    payment = request.GET.get('payment')
    date_from = request.GET.get('date_from')
    
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if status:
        orders = orders.filter(status=status)
    
    if payment == 'paid':
        orders = orders.exclude(stripe_payment_id='')
    elif payment == 'pending':
        orders = orders.filter(stripe_payment_id='')
    
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    
    # Stats
    total_orders = orders.count()
    total_revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
    avg_order_value = orders.aggregate(avg=Avg('total_price'))['avg'] or 0
    pending_orders = orders.filter(status='pending').count()
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value,
        'pending_orders': pending_orders,
    }
    return render(request, 'admin/order_list.html', context)

@login_required
@user_passes_test(is_admin)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/order_detail.html', {'order': order})

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related('profile').annotate(
        order_count=Count('order'),
        total_spent=Sum('order__total_price')
    )
    
    # Filtering
    search = request.GET.get('search')
    status = request.GET.get('status')
    date_joined = request.GET.get('date_joined')
    orders = request.GET.get('orders')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    elif status == 'staff':
        users = users.filter(is_staff=True)
    elif status == 'superuser':
        users = users.filter(is_superuser=True)
    
    if date_joined == 'today':
        users = users.filter(date_joined__date=timezone.now().date())
    elif date_joined == 'week':
        users = users.filter(date_joined__gte=timezone.now() - timedelta(days=7))
    elif date_joined == 'month':
        users = users.filter(date_joined__gte=timezone.now() - timedelta(days=30))
    elif date_joined == 'year':
        users = users.filter(date_joined__gte=timezone.now() - timedelta(days=365))
    
    if orders == 'with_orders':
        users = users.filter(order_count__gt=0)
    elif orders == 'without_orders':
        users = users.filter(order_count=0)
    
    # Stats
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    new_users_today = users.filter(date_joined__date=timezone.now().date()).count()
    users_with_orders = users.filter(order_count__gt=0).count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'new_users_today': new_users_today,
        'users_with_orders': users_with_orders,
    }
    return render(request, 'admin/user_list.html', context)

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'admin/user_detail.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def faq_list(request):
    faqs = FAQ.objects.select_related('category').all()
    
    # Filtering
    search = request.GET.get('search')
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    language = request.GET.get('language')
    
    if search:
        faqs = faqs.filter(
            Q(question__icontains=search) |
            Q(answer__icontains=search)
        )
    
    if category_id:
        faqs = faqs.filter(category_id=category_id)
    
    if status == 'published':
        faqs = faqs.filter(is_published=True)
    elif status == 'draft':
        faqs = faqs.filter(is_published=False)
    
    if language:
        faqs = faqs.filter(language=language)
    
    # Stats
    total_faqs = faqs.count()
    published_faqs = faqs.filter(is_published=True).count()
    draft_faqs = faqs.filter(is_published=False).count()
    total_categories = Category.objects.count()
    
    # Popular and recent FAQs
    popular_faqs = faqs.order_by('-view_count')[:5]
    recent_faqs = faqs.order_by('-updated_at')[:5]
    
    context = {
        'faqs': faqs,
        'categories': Category.objects.all(),
        'total_faqs': total_faqs,
        'published_faqs': published_faqs,
        'draft_faqs': draft_faqs,
        'total_categories': total_categories,
        'popular_faqs': popular_faqs,
        'recent_faqs': recent_faqs,
    }
    return render(request, 'admin/faq_list.html', context)

@login_required
@user_passes_test(is_admin)
def faq_create(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save()
            messages.success(request, 'FAQ created successfully!')
            return redirect('admin:faq_list')
    else:
        form = FAQForm()
    
    return render(request, 'admin/faq_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def faq_edit(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ updated successfully!')
            return redirect('admin:faq_list')
    else:
        form = FAQForm(instance=faq)
    
    return render(request, 'admin/faq_form.html', {'form': form, 'faq': faq})

@login_required
@user_passes_test(is_admin)
def faq_delete(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ deleted successfully!')
        return redirect('admin:faq_list')
    
    return render(request, 'admin/faq_confirm_delete.html', {'faq': faq})

# AJAX Views
@require_POST
@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
        order.status = new_status
        order.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid status'})

@require_POST
@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    activate = request.POST.get('activate') == 'true'
    
    user.is_active = activate
    user.save()
    
    return JsonResponse({'success': True})

@require_POST
@login_required
@user_passes_test(is_admin)
def toggle_faq_status(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.is_published = not faq.is_published
    faq.save()
    
    return JsonResponse({'success': True})

# Export Views
@login_required
@user_passes_test(is_admin)
def export_orders(request):
    orders = Order.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Email', 'Total', 'Status', 'Date'])
    
    for order in orders:
        writer.writerow([
            order.id,
            f"{order.first_name} {order.last_name}",
            order.email,
            order.total_price,
            order.status,
            order.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

@login_required
@user_passes_test(is_admin)
def export_users(request):
    users = User.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Active', 'Staff', 'Date Joined'])
    
    for user in users:
        writer.writerow([
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.is_active,
            user.is_staff,
            user.date_joined.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response
