from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import stripe
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Create Stripe payment intent
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(order.total_price * 100),  # Convert to cents
                    currency='usd',
                    metadata={'order_id': order.id}
                )
                return render(request, 'orders/payment.html', {
                    'order': order,
                    'client_secret': intent.client_secret,
                    'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
                })
            except stripe.error.StripeError as e:
                messages.error(request, f'Payment error: {str(e)}')
                return redirect('orders:checkout')
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

def payment_success(request):
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'confirmed'
        order.save()
        messages.success(request, 'Payment successful! Your order has been confirmed.')
    return redirect('orders:order_list')
