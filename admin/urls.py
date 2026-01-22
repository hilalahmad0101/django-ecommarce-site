from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/export/', views.export_orders, name='export_orders'),
    
    # User URLs
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/export/', views.export_users, name='export_users'),
    
    # FAQ URLs
    path('faqs/', views.faq_list, name='faq_list'),
    path('faqs/create/', views.faq_create, name='faq_create'),
    path('faqs/<int:faq_id>/edit/', views.faq_edit, name='faq_edit'),
    path('faqs/<int:faq_id>/delete/', views.faq_delete, name='faq_delete'),
    
    # AJAX URLs
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('faqs/<int:faq_id>/toggle-status/', views.toggle_faq_status, name='toggle_faq_status'),
]
