from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('adminsignout', views.adminsignout, name='adminsignout'),
    path('adminside', views.adminside, name='adminside'),
    path('sample', views.sample, name='sample'),
    path('dashboard', views.dashboard, name='dashboard'),

    ###User management side###
    path('products', views.products, name='products'),
    path('admin_user_search', views.admin_user_search, name='admin_user_search'),
    path('admin_block_unblock', views.admin_block_unblock, name='admin_block_unblock'),
   
   
    ###category management side###
    path('categorymanagement', views.categorymanagement, name='categorymanagement'),
    path('admin_category_search', views.admin_category_search, name='admin_category_search'),
    path('addcategory', views.addcategory,name='addcategory'),
    path('updatecategory/<str:id>', views.updatecategory,name='updatecategory'),
    path('deletecategory/<str:id>', views.deletecategory,name='deletecategory'),
    
    ###Product management side###
    path('productmanagement', views.productmanagement, name='productmanagement'),
    path('admin_product_search', views.admin_product_search, name='admin_product_search'),
    path('addproduct', views.addproduct,name='addproduct'),
    path('updateproduct/<str:id>', views.updateproduct,name='updateproduct'),
    path('deleteproduct/<str:id>', views.deleteproduct,name='deleteproduct'),
    
    ###variant management side###
    path('variants/<product_id>', views.variants, name='variants'),
    path('addvariants/<product_id>', views.addvariants,name='addvariants'),
    path('updatevariants/<str:id>', views.updatevariants,name='updatevariants'),
    path('deletevariants/<str:id>', views.deletevariants,name='deletevariants'),
    

    path('order_list', views.order_list,name='order_list'),
    path('item_details/<order_id>', views.item_details, name='item_details'),
    path('admin_change_order_status/<order_id>/', views.admin_change_order_status, name='admin_change_order_status'),
    path('stock_availability', views.stock_availability,name='stock_availability'),
    path('updatestock/<str:id>', views.updatestock,name='updatestock'),
    
    
    ###coupon management side###
    path('coupon_management', views.coupon_management, name='coupon_management'),
    path('addcoupon', views.addcoupon,name='addcoupon'),
    path('updatecoupon/<str:id>', views.updatecoupon,name='updatecoupon'),
    path('deletecoupon/<str:id>', views.deletecoupon,name='deletecoupon'),
    
    
    path('offer_management', views.offer_management,name='offer_management'),
    path('addoffer', views.addoffer,name='addoffer'),
    # path('updateoffer/<str:id>', views.updateoffer,name='updateoffer'),
    path('deleteoffer/<str:id>', views.deleteoffer,name='deleteoffer'),
    
    path('graph_chart_management', views.graph_chart_management,name='graph_chart_management'),
    path('sales_management', views.sales_management,name='sales_management'),
    path('filtered_sales', views.filtered_sales,name='filtered_sales'),
    path('order_summary/<order_id>', views.order_summary, name='order_summary'),
    path('chart_management', views.chart_management,name='chart_management'),
    
    
]