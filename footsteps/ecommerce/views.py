import json
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from ecommerce.models import *
from adminside.models import *
from cart.models import *
from django.contrib.auth import authenticate, login,logout
from adminside.views import *
from django.shortcuts import render, redirect

from .utils import generate_otp, send_otp_email
from django.core.mail import EmailMessage
from django.utils import timezone
from django.db.models import Q
from cart.views import _cart_id
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from datetime import date 
import datetime
from django.conf import settings

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')[:8]
    context = {
        'products': products,
    }
    return render(request, "ecommerce/index.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Userprofile.objects.get(email=email, password=password)
            if user.is_blocked:
                messages.error(request,"Your Blocked by the Administration department ")
                return redirect("home")
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass
                otp = generate_otp()
                send_otp_email(email, otp)
                request.session['session_otp'] = otp
                request.session['username']=email
                request.session['password']=password
                return render(request,'ecommerce/validateOTP.html')
        except:
            error_message = 'Invalid username or password'
    else:
        error_message = 'error'
    return render(request, 'ecommerce/signin.html', {'error_message': error_message})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        # Retrieve data from the form
        referral_id = generate_unique_referral_id()
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        password = request.POST['password']
        referral_code = request.POST['referral_code']
        # Create a new user object and save it to the database
        if User.objects.filter(username=email).exists():
            messages.warning(request,"Email is already Exist Please try another Mail")
            return redirect('signup')
        if referral_code:
            try:
                referrer = Userprofile.objects.get(referral_id=referral_code)
                # Credit the new user's wallet
                user = User.objects.create_user(username=email,password=password,first_name=first_name,last_name=last_name)
                user.save()
                emp = Userprofile(user=user,email=email,firstname=first_name,mobile = mobile,lastname=last_name,password=password,referral_id=referral_id)
                emp.save()
                user_wallet = Wallet(user=emp)
                user_wallet.amount = 50  # Adjust the amount as needed
                user_wallet.save()
                # Credit the referrer's wallet
                referrer_wallet = Wallet.objects.get(user=referrer)
                referrer_wallet.amount += 50  # Adjust the amount as needed
                referrer_wallet.save()
            except Userprofile.DoesNotExist:
                user = User.objects.create_user(username=email,password=password,first_name=first_name,last_name=last_name)
                user.save()
                emp = Userprofile(user=user,email=email,firstname=first_name,mobile = mobile,lastname=last_name,password=password,referral_id=referral_id)
                emp.save()
                user_wallet = Wallet(user=emp,amount=0)
                user_wallet.save()
                messages.error(request, 'Invalid referral code.')
        else:
            try:
                user = User.objects.create_user(username=email,password=password,first_name=first_name,last_name=last_name)
                user.save()
                emp = Userprofile(user=user,email=email,firstname=first_name,mobile = mobile,lastname=last_name,password=password,referral_id=referral_id)
                emp.save()
                user_wallet = Wallet(user=emp,amount=0)
                user_wallet.save()
            except:
                pass
        return redirect('signin')
    return render(request,"ecommerce/signup.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
        request.session.clear()
        logout(request)
        messages.success(request,"Logged Out successfully")
        return redirect('home')
    
    
import random
import string
def generate_unique_referral_id(length=8):
    # Define the set of characters to choose from (alphanumeric)
    characters = string.ascii_letters + string.digits
    # Generate a random ID until a unique one is found
    while True:
        referral_id = ''.join(random.choice(characters) for _ in range(length))
        # Check if the generated referral ID is unique (e.g., by querying your database)
        # If it's unique, return it; otherwise, generate a new one
        if not Userprofile.objects.filter(referral_id=referral_id).exists():
            return referral_id
    
  
def shop(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = { 
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'ecommerce/shop.html', context)



def product_details(request,product_id):
    product = Product.objects.get(id = product_id)
    products = Product.objects.all().filter(is_available=True)[:4]
    # variation_list =  Variation.objects.filter(product = product)
    color =  ColorVariant.objects.filter(product_id = product_id)
    size3 =  SizeVariant.objects.filter(product_id = product_id,)
    size_set = set()
    for size in size3:
        size_set.add(size.size)
    size_list = list(size_set)  
    size_list.sort()
    context = {
        'products': products,
        'product':product,
        'color':color,
        'size':size_list,
    }
    return render(request, 'ecommerce/product_details.html',context)




def loadsize(request):
    color_id = request.GET.get('colorid')
    color=ColorVariant.objects.get(id = color_id)
    sizelist=SizeVariant.objects.filter(Color_id = color)
    context={
        'sizelist':sizelist
    }
    return render(request, 'ecommerce\size.html',context)



def show_avalibality(request):
    size_id = request.GET.get('size_id')
    item = SizeVariant.objects.get(id=size_id)
    context = {"stock":item.stock}
    return render(request, 'ecommerce/availability.html',context)

def otp_verification_view(request):
    if request.method == 'POST':
        # Process the OTP form data
        user_entered_otp = request.POST.get('otp')
        otp =request.session['session_otp']
        if user_entered_otp==otp:
            username=request.session['username']
            password=request.session['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'OTP Verified Successfully')
        else:
            messages.success(request, 'OTP Verification Failed')    
        return redirect('home')  # Replace with your dashboard URL
    return render(request, 'validateOTP.html')

def search(request,category_slug=None):
    query = request.GET['query']
    products = Product.objects.filter(product_name__icontains=query)
    context = {
        'query': query,
        'products': products,     
    }
    return render (request,'ecommerce/shop.html',context)




@login_required(login_url='signin')
def userdashboard(request):
    current_user = request.user
    user = Userprofile.objects.get(user=current_user)
    # order = Order.objects.filter(user_id=request.user.id,is_ordered =True)
    order = Order.objects.filter(user_id=user,is_ordered =True)
    orders_count = order.count()
    context = {
        'user1':user,
        'orders_count':orders_count
    }
    return render(request, 'ecommerce/dashboard.html',context)

@login_required(login_url='signin')
def my_orders(request):
    current_user = request.user
    user = Userprofile.objects.get(user=current_user)
    orders = Order.objects.filter(user_id=user,is_ordered =True).order_by('-created_at')
    paginator = Paginator(orders, 11)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = orders.count()
    
    # orders = Order.objects.filter(user_id=request.user.id,is_ordered =True).order_by('-created_at')
    context = {
        'orders':paged_products,
        'product_count':product_count
        
    }
    return render(request, 'ecommerce/my_orders.html',context)

def invoice_details(request,order_id):
    orders = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=orders)
    # Calculate the Grand Total
    grand_total = orders.order_total - orders.discount_Price
    context ={
        # 'discount':discount,
        "order_items":order_items,
        'orders':orders,
        'grand_total':round(grand_total,2)  
    }
    return render(request,'ecommerce/invoice.html',context)


def details(request,order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=order)
    context ={
        "order_items":order_items
    }
    return render(request,'ecommerce/details.html',context)

def cancel_order(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status ="Cancelled"
    order.save()
    
    return redirect('my_orders')


@login_required(login_url='signin')
def edit_profile(request):
    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        userprofile = Userprofile.objects.get(user=current_user)
        user.username=email
        userprofile.firstname=firstname
        userprofile.lastname=lastname
        userprofile.mobile=mobile
        user.save()
        userprofile.save() 
        return redirect('edit_profile')  
    else:
        current_user = request.user
        userprofile = Userprofile.objects.get(user=current_user)
        context = {
            'user1':userprofile, 
        }
    return render(request,'ecommerce/edit_profile.html',context)


###Address management side###
###-----Start-----###

# @login_required(login_url='')
def addressmanagement(request):
    current_user = request.user
    user = Userprofile.objects.get(user=current_user)
    address = Profile.objects.filter(user_id=user)
    context = {'address':address
                }
    return render(request,'ecommerce/add_address.html',context)


# @login_required(login_url='')
def add_address(request):
    if request.method =='POST':
        current_user = request.user
        user = Userprofile.objects.get(user=current_user)
        address_line_1 = request.POST.get('address_line_1')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address_l = Profile.objects.filter(user_id=user)
        for adrs in address_l:
            adrs.is_default=False
            adrs.save()
        address = Profile(user=user,
            address_line_1= address_line_1,
            address_line_2= address_line_2,
            city=city,
            state=state,
            country=country,
            is_default=True)
        address.save()
        return redirect('addressmanagement')
    address=Profile.objects.all()
    context={'address':address}
    return render(request,'ecommerce/add_address.html',context)
      
 
# @login_required(login_url='')  
def update_address(request,id):
    if request.method =='POST':
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address = Profile.objects.get(id=id)
        address.address_line_1 = address_line_1
        address.address_line_2 = address_line_2
        address.city=city
        address.state=state
        address.country=country
        address.save()  
        return redirect('addressmanagement')
    return render(request,'ecommerce/add_address.html') 
        
          
            
  
# @login_required(login_url='')  
def delete_address(request,id):
    emp = Profile.objects.filter(id = id)
    emp.delete()
    context ={
        'emp':emp,
    }
    return redirect('addressmanagement') 

###Address management side###
###-----End-----###


@login_required(login_url='signin')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Userprofile.objects.get(email=request.user.username)
        user1 = User.objects.get(username=request.user.username)
        if new_password == confirm_password:
            sucess = user.password == current_password #user.check_password(current_password)
            if sucess:
                user.password = new_password #set_password(new_password)
                user1.set_password(new_password)
                user.save()
                user1.save()
                messages.success(request,'Password Update Sucessfully')
                login(request, user1)
                return redirect('change_password')
            else:
                messages.error(request,'Current Password is Wrong')
                return redirect('change_password')
        else:
            messages.error(request,"Passwords doesn't match")
            return redirect('change_password')            
    return render(request,'ecommerce/change_password.html')



# from .forms import OrderForm
def place_order(request, total=0, quantity=0,):
    current_user = request.user
    user=Userprofile.objects.get(user=current_user)
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')

    grand_total = 0
    tax = 0
    
    for cart_item in cart_items:
        total += (cart_item.variations.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    if request.method == 'POST':
        # Extract form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        order_note = request.POST.get('order_note')
        
        # Store all the billing information inside Order table
        data = Order()
        data.user = user
        data.first_name = first_name
        data.last_name = last_name
        data.phone = phone
        data.email = email
        data.address_line_1 = address_line_1
        data.address_line_2 = address_line_2
        data.country = country
        data.state = state
        data.city = city
        data.order_note = order_note
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")  # 20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        wallet = Wallet.objects.get(user=user)
        order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
        user=Userprofile.objects.get(user=current_user)
        for cart_item in cart_items:
            ord = OrderProduct(order=order,user=user,
                               product=cart_item.product,
                               variations=cart_item.variations,
                               quantity=cart_item.quantity,
                               product_price=cart_item.variations.price*cart_item.quantity)
            ord.save()
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
            'wallet.amount':wallet.amount,
            'discount_price':0
        }
        return render(request, 'ecommerce/payments.html', context)
    else:
        return redirect('checkout')




def payments1(request):
    current_user = request.user
    user=Userprofile.objects.get(user=current_user)
    discount_price = request.GET.get('discount_price')
    body = json.loads(request.body)
    payment = Payment(
            user = user,
            payment_id = body['transID'],
            payment_method = body['payment_method'],
            amount_paid = body['payedAmount'],
            status = body['status'],
            
        )
    payment.save()
    order = Order.objects.get(user=user, is_ordered=False, id=body['orderID'])
    order.payment = payment
    order.is_ordered = True
    order.discount_Price=body['discountprice']
    order.discount_amount = float(order.order_total) - float(body['discountprice'])
    order.save()
    
    # Move the cart items to Order Product table
    order_items = OrderProduct.objects.filter(order=order)

    for item in order_items:
        item.payment = payment
        item.ordered = True
        item.save()
    # Clear cart
    cart=CartItem.objects.filter(user=current_user)
    cart.delete()
    
    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    discount_price = request.GET.get('discount_price')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        

        subtotal = 0
        current_user = request.user
        user=Userprofile.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(user=current_user)
        for i in ordered_products:
            subtotal += i.variations.price * i.quantity
        payment = Payment.objects.get(payment_id=transID)
        order.payment_No=transID
        order.save()
        if  discount_price:
        # total=order.order_total-discount_price
            discount_price = float(discount_price)
            order.discount_Price=discount_price
            total = order.order_total - discount_price
            order.discount_amount=total
            order.save()
        grand_total= order.order_total - order.discount_Price

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'grand_total':round(grand_total,2),
            
        }
        return render(request, 'ecommerce/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
    





def cash_on_delivery(request, order_id):
    discount_price = request.GET.get('discount_price')
    current_user = request.user
    order = Order.objects.get(id=order_id)
    order.is_ordered = True
    order_products = OrderProduct.objects.filter(order=order)
    order_products.update(ordered=True)
    user= Userprofile.objects.get(user=current_user)
    payment = Payment(user= user,payment_method ="Cash On Delivery")
    payment.save()
    order.payment=payment
    order.save()
    order_items = OrderProduct.objects.filter(order=order)
    for item in order_items:
        item.payment = payment
        item.ordered = True
        item.save()
    if  discount_price:
        # total=order.order_total-discount_price
        discount_price = float(discount_price)
        order.discount_Price=discount_price
        total = order.order_total - discount_price
        order.discount_amount=total
        order.save()
    else:
        order.discount_amount=order.order_total
        order.discount_price=0
        order.save()
    cart=CartItem.objects.filter(user=current_user)
    cart.delete() 
    context = {'order':order}
    return redirect(my_orders)

def coupon_bazzer(request):
    coupons = Coupon.objects.filter(expdate__gte=date.today())
    context = {'coupons':coupons
                }
    return render(request,'ecommerce/coupon_display.html',context)

def coupon_payment(request,order_id):
    current_user = request.user
    order=Order.objects.get(id=order_id)
    user=Userprofile.objects.get(user=current_user)
    cart_items=CartItem.objects.filter(user=current_user)
    
    
    grand_total = 0
    tax = 0
    total = 0
    quantity = 0
    
    for cart_item in cart_items:
        total += (cart_item.variations.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'ecommerce/payments.html', context)

def coupon_check(request):
    if request.method == 'POST':
        current_user=request.user
        coupon = request.POST.get('coupon_obj')
        order_id = request.POST.get('order_id')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        user=Userprofile.objects.get(user=current_user)
        
        if not coupon_obj.exists() or len(coupon_obj)!=1:
            messages.warning(request,'Invalid Coupon')
            return redirect('coupon_payment', order_id)

        
        discount_price = 0
        couponobj = Coupon.objects.get(coupon_code__icontains = coupon)
        
        
        if CouponApplied.objects.filter(user_name=user, coupon_name=couponobj).exists():
            messages.info(request, 'Coupon is already applied to this order.')
            return redirect('coupon_payment', order_id)
            
        applied = CouponApplied(user_name=user, coupon_name=couponobj)
        applied.save()
        
        discount_price = couponobj.discount_price
        
        order=Order.objects.get(id=order_id)
        
        cart_items=CartItem.objects.filter(user=current_user)
        
        grand_total = 0
        tax = 0
        total = 0
        quantity = 0
        
        for cart_item in cart_items:
            total += (cart_item.variations.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = order.order_total - couponobj.discount_price

        context = {
            'discount_price':discount_price,
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': round(grand_total, 2),
        }
        return render(request, 'ecommerce/payments.html', context)

    context ={
        "coupon_obj":coupon_obj
    }
    return render(request,'ecommerce/payments.html',context)




def filtered_price(request):
    # Get the minimum and maximum price values from the request parameters
    min_price = request.GET.get('minamount')
    max_price = request.GET.get('maxamount')
    
    min_amount=min_price
    max_amount=max_price
    
    min_price=min_price.replace('$','')
    max_price=max_price.replace('$','')

    # Filter products based on the price range
    if min_price is not None and max_price is not None:
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    else:
        # Handle the case where no price range is provided
        products = Product.objects.all()

    context = {
        "products": products,
        "min_amount":min_amount,
        "max_amount":max_amount
        
    }

    return render(request, 'ecommerce/shop.html', context)

def wallet(request):
    current_user = request.user
    user = Userprofile.objects.get(user=current_user)
    wallet = Wallet.objects.get(user=user)

    context = {
                'user1':user,
                'wallet':wallet
                }
    return render(request, 'ecommerce/wallet.html',context)

def wallet_payment(request,order_id):
    if request.method == 'POST':
        discount_price = request.POST.get('discount_price')
        grand_total = request.POST.get('grand_total') 
        current_user = request.user
        user = Userprofile.objects.get(user=current_user)
        wallet = Wallet.objects.get(user=user)
        if wallet.amount >= float(grand_total):
            order = Order.objects.get(id=order_id)
            order.is_ordered = True
            if  discount_price:
                # total=order.order_total-discount_price
                discount_price = float(discount_price)
                order.discount_Price=discount_price
                total = order.order_total - discount_price
                order.discount_amount=round(total,2)
                order.save()
            else:
                order.discount_amount=order.order_total
                order.discount_price=0
                order.save()
            user= Userprofile.objects.get(user=current_user)
            payment = Payment(user= user,payment_method ="Wallet Payment")
            payment.save()
            order.payment=payment
            order.save()
            wallet.amount -= float(grand_total)
            wallet.save()
            cart=CartItem.objects.filter(user=current_user)
            cart.delete()
            return redirect(my_orders)
        else:
            messages.error(request,'insufficient Money in Your Wallet')
            return redirect(place_order)
    
    











