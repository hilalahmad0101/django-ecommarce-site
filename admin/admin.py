from django.contrib import admin
from .models import ProductStats, CategoryStats, UserStats, FAQ

@admin.register(ProductStats)
class ProductStatsAdmin(admin.ModelAdmin):
    list_display = ['product', 'times_ordered', 'total_revenue', 'wishlist_count', 'last_ordered']
    list_filter = ['last_ordered']
    search_fields = ['product__name']
    readonly_fields = ['times_ordered', 'total_revenue', 'wishlist_count', 'last_ordered']

@admin.register(CategoryStats)
class CategoryStatsAdmin(admin.ModelAdmin):
    list_display = ['category', 'product_count', 'total_revenue', 'average_price']
    search_fields = ['category__name']
    readonly_fields = ['product_count', 'total_revenue', 'average_price']

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_count', 'total_spent', 'last_order_date']
    list_filter = ['last_order_date']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['order_count', 'total_spent', 'last_order_date']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'language', 'is_published', 'view_count', 'created_at']
    list_filter = ['category', 'language', 'is_published', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['is_published']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
