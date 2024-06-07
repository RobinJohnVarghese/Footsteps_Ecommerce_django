from django.contrib import admin
from django.urls import path
from . import views
from .views import *


############################

urlpatterns = [
    path('', views.home,name="home"),
    path('home', views.home,name="home"),
    path('search', views.search,name="search"),
    
    path('signup', views.signup,name="signup"),
    path('signin', views.signin,name="signin"),
    path('otp_verification', otp_verification_view, name='otp_verification'),
    path('signout', views.signout,name="signout"),

    # path('profile', views.profile,name="profile"),
    path('edit_profile', views.edit_profile,name="edit_profile"),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('wallet/', views.wallet, name='wallet'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('invoice_details/<order_id>/', views.invoice_details, name='invoice_details'),
    path('change_password/', views.change_password, name='change_password'),
    
    
    path('addressmanagement', views.addressmanagement, name='addressmanagement'),
    path('add_address', views.add_address,name='add_address'),
    path('update_address/<str:id>', views.update_address,name='update_address'),
    path('delete_address/<str:id>', views.delete_address,name='delete_address'),
    
    
    
    
    path('shop', views.shop,name="shop"),
    path('shop/<slug:category_slug>/', views.shop, name='products_by_category'),
    path('product_details/<product_id>', views.product_details,name="product_details"),
    # path('get_variant_price/', get_variant_price, name='get_variant_price'),
    path('loadsize', views.loadsize,name="loadsize"),
    path('show_avalibality', views.show_avalibality,name="show_avalibality"),

    
    
    path('place_order', views.place_order,name="place_order"),
    path('payments', views.payments1,name="payments"),
    path('cash_on_delivery/<order_id>/', views.cash_on_delivery,name="cash_on_delivery"), 
    path('wallet_payment/<order_id>/', views.wallet_payment,name="wallet_payment"),
    path('details/<order_id>/', views.details, name='details'),
    path('cancel_order/<order_id>/', views.cancel_order, name='cancel_order'),
    
    
    path('filtered_price', views.filtered_price, name='filtered_price'),
    path('order_complete/', views.order_complete, name='order_complete'),

    path('coupon_check', views.coupon_check, name='coupon_check'),
    path('coupon_bazzer', views.coupon_bazzer, name='coupon_bazzer'),
    path('coupon_payment/<order_id>/', views.coupon_payment, name='coupon_payment'),
    
    
]
