from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('category/<slug:category_slug>/', views.product_list, name='product_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/change_quantity/', views.change_quantity, name='change_quantity'),
    
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    path('prodotti/', views.product_list, name='product_list'),
    path('servizi/', views.servizi, name='servizi'),
    path('chi-siamo/', views.chi_siamo, name='chi_siamo'),
    path('contatti/', views.contatti, name='contatti'),
]