from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        # return format_html ('<img src = "{}" width = "30" style ="bordar-radius:50%;">'.format (object:profile_picture.url))
        # return format_html('<img src="{}" width="30" style="border-radius: 50%;">', object.profile_picture.url)
        # formatted_image = format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(profile_picture.url))
        # return formatted_image
        formatted_image = format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(object.profile_picture.url))
        return formatted_image
    
    thumbnail.short_disctription = 'profile picture'
    list_display = ('user', 'city', 'state', 'country')
admin.site.register(Profile,ProfileAdmin)

    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid' ,'status', 'created_at',)
admin.site.register(Payment,PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'order_number', 'payment' , 'order_total','tax','discount_amount','discount_Price','created_at', 'status', )
admin.site.register(Order,OrderAdmin)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code','expdate', 'discount_price', 'minimum_amount' )
admin.site.register(Coupon,CouponAdmin)

class CouponAppliedAdmin(admin.ModelAdmin):
    list_display = ('coupon_name','user_name' )
admin.site.register(CouponApplied,CouponAppliedAdmin)


class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user','full_name', 'mobile', 'password','referral_id','is_blocked' )
admin.site.register(Userprofile,UserprofileAdmin)
# admin.site.register(Userprofile)

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment', 'user', 'product' ,'quantity', 'created_at',)
admin.site.register(OrderProduct,OrderProductAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'referral_id', 'referrer' ,'updated_at')
admin.site.register(Wallet,WalletAdmin)