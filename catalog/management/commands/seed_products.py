from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create products
        products_data = [
            {'name': 'Laptop Pro', 'category': 'Electronics', 'price': '999.99', 'stock': 10, 'description': 'High-performance laptop for professionals'},
            {'name': 'Wireless Headphones', 'category': 'Electronics', 'price': '199.99', 'stock': 25, 'description': 'Premium noise-cancelling headphones'},
            {'name': 'Smart Watch', 'category': 'Electronics', 'price': '299.99', 'stock': 15, 'description': 'Feature-rich smartwatch with health tracking'},
            {'name': 'T-Shirt', 'category': 'Clothing', 'price': '29.99', 'stock': 50, 'description': 'Comfortable cotton t-shirt'},
            {'name': 'Jeans', 'category': 'Clothing', 'price': '79.99', 'stock': 30, 'description': 'Classic denim jeans'},
            {'name': 'Python Programming', 'category': 'Books', 'price': '39.99', 'stock': 20, 'description': 'Learn Python programming from scratch'},
            {'name': 'Garden Tools Set', 'category': 'Home & Garden', 'price': '49.99', 'stock': 12, 'description': 'Complete set of essential garden tools'},
            {'name': 'Yoga Mat', 'category': 'Sports', 'price': '29.99', 'stock': 35, 'description': 'Non-slip exercise yoga mat'},
        ]

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'price': Decimal(prod_data['price']),
                    'stock': prod_data['stock'],
                    'description': prod_data['description'],
                    'available': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
