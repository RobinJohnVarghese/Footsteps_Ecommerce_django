from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','real_price', 'price', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)

# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product','image')
    

# admin.site.register(ProductImage)


# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variation_category', 'variation_value', 'is_active')
#     list_editable = ('is_active',)
#     list_filter = ('product', 'variation_category', 'variation_value')

# admin.site.register(Variation,VariationAdmin)


# class ColorVariationAdmin(admin.ModelAdmin):
#     list_display = ('product_id', 'colour')
#     list_editable = ('is_active',)
    # list_filter = ('product', 'variation_category', 'variation_value')
admin.site.register(ColorVariant)


class SizeVariationAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'Color_id', 'size','real_price', 'price','stock')
    # list_editable = ('is_active',)
    # list_filter = ('product', 'variation_category', 'variation_value')
admin.site.register(SizeVariant,SizeVariationAdmin)
list_display = ('product_id', 'Color_id', 'size', 'price','stock')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('category', 'discount', 'end_date')
admin.site.register(Offer,OfferAdmin)
