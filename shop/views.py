from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        session_key = request.session.session_key
        if session_key:
            try:
                anon_cart = Cart.objects.get(session_key=session_key, user=None)
                for item in anon_cart.items.all():
                    existing_item = CartItem.objects.filter(cart=cart, product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = cart
                        item.save()
                anon_cart.delete()
            except Cart.DoesNotExist:
                pass

    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)

    return cart

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'category_name': category.name if category else None,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query)
        )
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'query': query
    })

def cart_detail(request):
    cart = get_cart(request)
    items = cart.items.all()
    
    items.filter(product__available=False).delete()
    items = items.filter(product__available=True)

    subtotal = sum(Decimal(item.product.price) * item.quantity for item in items)
    shipping_cost = Decimal('5.00') 
    discount = Decimal('0.00')
    
    if request.user.is_authenticated:
        shipping_cost = Decimal('0.00')
        
        if not Order.objects.filter(user=request.user).exists():
            discount = subtotal * Decimal('0.10')
            discount = discount.quantize(Decimal('0.00'))

    total = subtotal - discount + shipping_cost

    return render(request, 'shop/cart.html', {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'shipping_cost': shipping_cost,
        'total': total,
        'user_is_authenticated': request.user.is_authenticated
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('shop:cart_detail')

def remove_from_cart(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('shop:cart_detail')

def update_cart_item(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        except ValueError:
            pass 

    return redirect('shop:cart_detail')

class CheckoutView(View):
    def get(self, request):
        cart = get_cart(request)
        items = cart.items.all()
        
        subtotal = sum(Decimal(item.product.price) * item.quantity for item in items)
        
        discount = Decimal('0.00')
        shipping_cost = Decimal('5.00') 
        
        if request.user.is_authenticated:
            shipping_cost = Decimal('0.00') 
            
            if not Order.objects.filter(user=request.user).exists():
                discount = subtotal * Decimal('0.10')
                discount = discount.quantize(Decimal('0.00')) 
        
        total = subtotal - discount + shipping_cost
        
        form = CheckoutForm()
        
        return render(request, 'shop/checkout.html', {
            'cart': cart,
            'items': items,
            'subtotal': subtotal,
            'discount': discount,
            'shipping_cost': shipping_cost,
            'total': total,
            'form': form
        })
        
    def post(self, request):
        cart = get_cart(request)
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            original_subtotal = sum(Decimal(item.product.price) * item.quantity for item in cart.items.all())
            discount = Decimal('0.00')
            
            shipping_cost = Decimal('5.00') if not request.user.is_authenticated else Decimal('0.00')
            
            if request.user.is_authenticated and not Order.objects.filter(user=request.user).exists():
                discount = original_subtotal * Decimal('0.10')

            subtotal = original_subtotal - discount
            total = subtotal + shipping_cost
            
            order.total = round(total, 2)
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.discount_price if item.product.discount_price else item.product.price,
                    quantity=item.quantity
                )
            
            cart.items.all().delete()
            return redirect('shop:order_confirmation', order_id=order.id)
        
        return render(request, 'shop/checkout.html', {
            'cart': cart,
            'form': form
        })

@require_POST
def change_quantity(request):
    cart = get_cart(request)
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        cart_item.save()
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'item_total': round(cart_item.get_total_price(), 2)
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user and request.user != order.user:
        return redirect('shop:product_list')
    return render(request, 'shop/order_confirmation.html', {'order': order})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return redirect('shop:product_list')
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('date_created')
    return render(request, 'shop/order_history.html', {'orders': orders})

def servizi(request):
    return render(request, 'servizi.html')

def chi_siamo(request):
    return render(request, 'chi_siamo.html')

def contatti(request):
    return render(request, 'contatti.html')