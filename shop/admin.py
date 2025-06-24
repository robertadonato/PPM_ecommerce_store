from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'category', 'is_new', 'available']
    list_filter = ['category', 'is_new', 'available']
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'total', 'paid', 'status', 'date_created']
    list_filter = ['paid', 'status', 'date_created']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)