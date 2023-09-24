from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from adminside.models import *
from ecommerce.models import *
from django.conf import settings
import uuid
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Userprofile(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100 )
    is_blocked =models.BooleanField(default=False)
    referral_id = models.CharField(max_length=8,null=True,blank=True,unique=True)
    otp = models.CharField(max_length=15)
    
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    def __str__(self):
        return self.firstname
    
    
class Profile(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True,max_length=100)
    address_line_2 = models.CharField(blank=True,max_length=100)
    profile_picture = models.ImageField(upload_to='userprofile', blank=True)
    city = models.CharField(blank=True,max_length=100)
    state = models.CharField(blank=True,max_length=100)
    country = models.CharField(blank=True,max_length=100)
    is_default= models.BooleanField()
        

    def __str__(self):
        return self.user.firstname
    
    def full_address(self):
        return f'{self.address_line_1}  {self.address_line_2}, {self.city}, {self.state}, {self.country}'
    

# class Address(models.Model):
#     """
#     Address
#     """

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     customer = models.ForeignKey(Userprofile, verbose_name=_("Customer"), on_delete=models.CASCADE)
#     full_name = models.CharField(_("Full Name"), max_length=150)
#     phone = models.CharField(_("Phone Number"), max_length=50)
#     postcode = models.CharField(_("Postcode"), max_length=50)
#     address_line = models.CharField(_("Address Line 1"), max_length=255)
#     address_line2 = models.CharField(_("Address Line 2"), max_length=255)
#     town_city = models.CharField(_("Town/City/State"), max_length=150)
#     delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
#     created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
#     default = models.BooleanField(_("Default"), default=False)

#     class Meta:
#         verbose_name = "Address"
#         verbose_name_plural = "Addresses"

#     def __str__(self):
#         return "{} Address".format(self.full_name)


   
    
class Payment(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_method


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    payment_No = models.CharField(max_length=100,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    discount_amount = models.FloatField(blank=True,null=True,default=0)
    discount_Price = models.FloatField(blank=True,null=True,default=0)
    # amount_recived = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def full_address_d(self):
        return f'{self.address_line_1}, {self.address_line_2}, {self.city}, {self.state}, {self.country}'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(SizeVariant, on_delete=models.CASCADE,blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.first_name
    
    
    
from datetime import date   
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20)
    expdate = models.DateField(blank=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    
    def expiry_date(self):
        return str(self.expdate)
    
    def check_expiry(self):
        if self.expdate < date.today():
            return str("Expired")
        else:
            return str("Valid")
    def __str__(self):
            return self.coupon_code

class CouponApplied(models.Model):
    user_name = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=True)
    coupon_name = models.ForeignKey(Coupon,on_delete=models.CASCADE, null=True,max_length=20)
    
    def __str__(self):
            return f'{self.coupon_name.coupon_code}' 
        
class Wallet(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=50)
    referral_id = models.CharField(max_length=20, unique=True, null=True)
    referrer = models.ForeignKey(Userprofile, related_name='referrals', null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super().save(*args,**kwargs)
