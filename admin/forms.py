from django import forms
from catalog.models import Product, Category
from .models import FAQ

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'description', 'price', 'image', 'stock', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'slug': forms.TextInput(attrs={'placeholder': 'Leave empty to auto-generate'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'slug': forms.TextInput(attrs={'placeholder': 'Leave empty to auto-generate'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['category', 'question', 'answer', 'language', 'is_published']
        widgets = {
            'answer': forms.Textarea(attrs={'rows': 4}),
        }
