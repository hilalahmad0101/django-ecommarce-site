from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product, Category
from orders.models import Order

class ProductStats(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    times_ordered = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wishlist_count = models.PositiveIntegerField(default=0)
    last_ordered = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Stats for {self.product.name}"

class CategoryStats(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    product_count = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Stats for {self.category.name}"

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_count = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_order_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Stats for {self.user.username}"

class FAQ(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.question
