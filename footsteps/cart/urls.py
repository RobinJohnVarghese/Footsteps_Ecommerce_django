from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('select_address/<int:address_id>/', views.select_address, name='select_address'),
    path('get_cart_count', views.get_cart_count, name='get_cart_count'),
    path('inc_cart/<int:product_id>/<int:cart_item_id>/', views.inc_cart, name='inc_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    # path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]