from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from ecommerce.models import *
from adminside.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings
import os
from django.db.models import Max,Min,Count,Avg
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear,ExtractWeek,ExtractDay,TruncMonth
from django.utils.timezone import now
import calendar

# Create your views here.



def adminside(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email,password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return render(request,'adminside/base.html')
        else:
            messages.error(request, 'Invalid Username or Password')
            return render(request,'adminside/adminsignin.html')

    else:    
        return render(request,'adminside/adminsignin.html')
    


@login_required(login_url='adminside')
def adminsignout(request):
    if request.user.is_staff:
        request.session.clear()
        logout(request)
        messages.success(request,"Logged Out successfully")
    return redirect('adminside')
    

@login_required(login_url='adminside')
def sample(request):
    return render(request,'adminside/sample-page.html')

@login_required(login_url='adminside')
def dashboard(request):
    products=Product.objects.all()
    sizes=SizeVariant.objects.filter(stock__lte=5)
    context = {
        'sizes':sizes,
        "products":products
    }
    return render(request,'adminside/base.html',context)


def updatestock(request,id):
    if request.method =='POST':
        product_id = request.POST.get('product_id')
        new_color = request.POST.get('color')
        new_size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')                    
        size = SizeVariant.objects.get(id=id)
        color = size.Color_id
        color.color=new_color
        color.save()
        size.size=new_size
        size.price=price
        size.stock = stock 
        size.save()  
        return redirect('dashboard')
    return render(request,'adminside\base.html')



@login_required(login_url='adminside')
def products(request):
    customers = Userprofile.objects.all()
    return render(request,'adminside/products.html',{'customers':customers})


###User management side###
###-----Start-----###
@login_required(login_url='adminside')
def admin_block_unblock(request):
    if request.method == 'GET' and 'id' in request.GET:
        user_id = request.GET['id']
        user = get_object_or_404(Userprofile, id=user_id)
        # Toggle the is_blocked status
        user.is_blocked = not user.is_blocked
        user.save()
        if user.is_blocked:
            messages.info(request, "User Account Blocked")
        else:
            messages.info(request, "User Account Unblocked")
    customers = Userprofile.objects.all()
    return render(request, 'adminside/products.html', {'customers': customers})

@login_required(login_url='adminside')
def products(request):
    customers = Userprofile.objects.all()
    return render(request,'adminside/products.html',{'customers':customers})

@login_required(login_url='adminside')
def admin_user_search(request):
    query = request.GET['query']
    custom = Userprofile.objects.filter(firstname__icontains=query)
    return render(request, 'adminside/products.html',{'customers': custom})#'ud1': ud1

###User management side###
###-----End-----###



###Category management side###
###-----Start-----###

@login_required(login_url='adminside')
def categorymanagement(request):
    categories = Category.objects.all()
    return render(request,'adminside/categorymanagement.html',{'categories':categories})

@login_required(login_url='adminside')
def admin_category_search(request):
    query = request.GET['query']
    cat = Category.objects.filter(category_name__icontains=query)
    return render(request, 'adminside/categorymanagement.html',{'categories': cat})

@login_required(login_url='adminside')
def addcategory(request):
    if request.method =='POST':
        category_name = request.POST.get('category_name')
        if Category.objects.filter(category_name=category_name).exists():
            error_message = 'Categoryname already exists. Please choose a different Categoryname.'
            return render(request, 'categorymanagement.html', {'error_message': error_message})
        else:
            category_name = request.POST.get('category_name')
            slug = request.POST.get('category_name')
            categories = Category(
                category_name= category_name,
                slug = slug,)
            categories.save()
            return redirect('categorymanagement')
    return render(request,'adminside\categorymanagement.html')

@login_required(login_url='adminside')     
def updatecategory(request,id):
    if request.method =='POST':
        category_name = request.POST.get('category_name')
        category = Category.objects.get(id=id)
        category.category_name = category_name
        category.slug=category_name
        category.save()
        return redirect('categorymanagement')
    return render(request,'adminside\categorymanagement.html', ) 

@login_required(login_url='adminside')
def deletecategory(request,id):
    category = Category.objects.filter(id = id)
    category.delete()
    return redirect('categorymanagement') 

###Category management side###
###-----End-----###


###Product management side###
###-----Start-----###

@login_required(login_url='adminside')
def productmanagement(request):
    products = Product.objects.all()
    categories=Category.objects.all()
    context = {'products':products,'categories':categories}
    return render(request,'adminside/productmanagement.html',context)

@login_required(login_url='adminside')
def admin_product_search(request):
    query = request.GET['query']
    product = Product.objects.filter(product_name__icontains=query)
    return render(request, 'adminside/productmanagement.html',{'products': product})

@login_required(login_url='adminside')
def addproduct(request):
    if request.method =='POST':
        product_name = request.POST.get('product_name')
        if Product.objects.filter(product_name=product_name).exists():
            error_message = 'Productname already exists. Please choose a different productname.'
            return render(request, 'productmanagenent.html',{'error_message': error_message})
        else:
            product_name = request.POST.get('product_name')
            slug = request.POST.get('product_name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            images = request.FILES['image']
            category_id = request.POST.get('category_id')
            category = Category.objects.get(id = category_id)
            products = Product(
                product_name= product_name,
                slug= slug,
                description=description,
                price=price,
                real_price=price,
                category=category)
            file_name = images.name
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb') as file:
                file.write(images.read())
            products.images = file_name
            products.save()
            return redirect('productmanagement')
    categories=Category.objects.all()
    context={'categories':categories}
    return render(request,'adminside\productmanagement.html',context)
      

@login_required(login_url='adminside')  
def updateproduct(request,id):
    if request.method =='POST':
        product_name = request.POST.get('product_name')
        slug = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id = category_id)   
        product = Product.objects.get(id=id)
        product.product_name = product_name
        product.slug = slug
        product.description=description
        product.price=price
        product.real_price=price
        product.category=category
        try:
            images = request.FILES['image']
            file_name = images.name
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb') as file:
                file.write(images.read())
            product.images = file_name
        except:
            pass
        product.save()  
        return redirect('productmanagement')
    return render(request,'adminside\productmanagement.html') 
           
  
@login_required(login_url='adminside')  
def deleteproduct(request,id):
    emp = Product.objects.filter(id = id)
    emp.delete()
    return redirect('productmanagement') 

###Product management side###
###-----End-----###





###variant management side###
###-----Start-----###
@login_required(login_url='adminside')
def variants(request,product_id):
    product=Product.objects.get(id=product_id)
    sizes=SizeVariant.objects.filter(product_id=product)
    context = {
        'sizes':sizes ,
        'product':product,  
    }
    return render(request,'adminside/variants.html',context)

@login_required(login_url='adminside')
def addvariants(request,product_id):
    if request.method =='POST':
        product_id = request.POST.get('product_id')
        color = request.POST.get('color')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        product=Product.objects.get(id=product_id)
        if ColorVariant.objects.filter(product_id=product,color=color).exists():
            color_v =ColorVariant.objects.get(product_id=product,color=color)
            size_v =SizeVariant(product_id=product,Color_id=color_v,size=size,stock=stock,price=price, real_price=price)
            size_v.save()
            return redirect('variants',product_id)
        else:
            color_v =ColorVariant(product_id=product,color=color)
            color_v.save()
            size_v =SizeVariant(product_id=product,Color_id=color_v,size=size,stock=stock,price=price, real_price=price)
            size_v.save()
            return redirect('variants',product_id)
    product_id = request.GET.get('product_id')
    return render(request,'adminside\variants.html')

@login_required(login_url='adminside')
def updatevariants(request,id):
    if request.method =='POST':
        product_id = request.POST.get('product_id')
        new_color = request.POST.get('color')
        new_size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')                   
        size = SizeVariant.objects.get(id=id)
        color = size.Color_id
        color.color=new_color
        color.save()
        size.size=new_size
        size.price=price
        size.real_price=price
        size.stock = stock
        size.save()  
        return redirect('variants',product_id)
    return render(request,'adminside\variants.html')

@login_required(login_url='adminside')
def deletevariants(request,id):
    emp = SizeVariant.objects.get(id=id)
    product_id=emp.product_id.id
    emp.delete()
    messages.warning(request,"Varient deleted Successfully")
    return redirect('variants',product_id) 

###variant management side###
###-----End-----###



@login_required(login_url='adminside')
def order_list(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    context ={
        "orders":orders
    }
    return render(request,'adminside/order_list.html',context)

@login_required(login_url='adminside')
def item_details(request,order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=order)
    context ={
        "order_items":order_items
    }
    return render(request,'adminside/item_details.html',context)

@login_required(login_url='adminside')
def admin_change_order_status(request,order_id):
    order = Order.objects.get(id=order_id)
    status = request.POST.get(f'status-{order_id}')
    order.status = status
    order.save()
    context ={
        "status":status
    }
    return redirect('order_list')#render(request,'adminside/operations.html',context)


def stock_availability(request):
    sizes=SizeVariant.objects.filter(stock__lte=5)
    context = {
        'sizes':sizes
    }
    return render(request,'adminside/base.html',context)


from django.db.models import Q
def sales_management(request):
    
    sales = Order.objects.filter(Q(is_ordered=True) & ~Q(status='Cancelled')).order_by('-created_at')
    paginator = Paginator(sales, 14)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = sales.count()
    context={
        'sales':paged_products,
        'product_count':product_count
    }
    return render(request,'adminside/sales_summary.html',context)

@login_required(login_url='adminside')
def order_summary(request,order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=order)
    
    context ={
        "order_items":order_items,
        'order':order
    }
    return render(request,'adminside/order_summary.html',context)


def filtered_sales(request):
    # Get the minimum and maximum price values from the request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    from_date = f'{start_date}+00:00'
    to_date = f'{end_date} 23:59:59+00:00'
    
    # Filter products based on the price range
    # if start_date is not None and end_date is not None:
    orders = Order.objects.filter(created_at__gte=from_date, created_at__lte=to_date)

    context = {
        "sales": orders,
        "start_date":start_date,
        "end_date":end_date
        
    }

    return render(request,'adminside\sales_summary.html',context)



###Coupon management side###
###-----Start-----###

@login_required(login_url='adminside')
def coupon_management(request):
    coupons=Coupon.objects.all()
    context = {
        'coupons':coupons ,
    }
    return render(request,'adminside/coupon_management.html',context)

@login_required(login_url='adminside')
def addcoupon(request):
    if request.method =='POST':
        coupon_code = request.POST.get('coupon_code')
        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            error_message = 'Coupon name already exists. Please choose a different Coupon name.'
            return render(request, 'coupon_management.html', {'error_message': error_message})
        else:
            coupon_code = request.POST.get('coupon_code')
            expdate = request.POST.get('is_expired')
            discount_price = request.POST.get('discount_price')
            minimum_amount = request.POST.get('minimum_amount')
            coupon = Coupon(coupon_code=coupon_code,
                expdate= expdate,
                discount_price= discount_price,
                minimum_amount=minimum_amount,
                )
            coupon.save()
            return redirect('coupon_management')
    return render(request,'adminside/coupon_management.html')

@login_required(login_url='adminside')
def updatecoupon(request,id):
    if request.method =='POST':
        coupon_code = request.POST.get('coupon_code')
        expdate = request.POST.get('is_expired')
        discount_price = request.POST.get('discount_price')
        minimum_amount = request.POST.get('minimum_amount')             
        coupon = Coupon.objects.get(id=id)
        coupon.coupon_code= coupon_code
        coupon.expdate= expdate
        coupon.discount_price= discount_price
        coupon.minimum_amount= minimum_amount
        coupon.save()  
        return redirect('coupon_management')
    return render(request,'adminside\coupon_management.html')

@login_required(login_url='adminside')
def deletecoupon(request,id):
    emp = Coupon.objects.get(id=id)
    emp.delete()
    messages.warning(request,"Coupon deleted Successfully")
    return redirect('coupon_management') 


###Coupon management side###
###-----End-----###





###Offer management side###
###-----Start-----###

@login_required(login_url='adminside')
def offer_management(request):
    offers=Offer.objects.all()
    categories=Category.objects.all()
    context = {
        'offers':offers ,
        'categories':categories
    }
    return render(request,'adminside/offers.html',context)

@login_required(login_url='adminside')
def addoffer(request):
    if request.method =='POST':
        category_id = request.POST.get('category_id')
        if Offer.objects.filter(category=category_id).exists():
            error_message = 'This category already have an Offer exists. Please choose a different Category.'
            messages.error(request,"This category already have an Offer exists. Please choose a different Category.")
            return redirect('offer_management')
        else:
            category_id = request.POST.get('category_id')
            discount = request.POST.get('discount_price')
            end_date = request.POST.get('is_expired')
            category = Category.objects.get(id=category_id)
            
            product_list = Product.objects.filter(category=category)
            for product in product_list:
                variants = SizeVariant.objects.filter(product_id=product)
                for variant in variants:
                    variant.price = variant.real_price - float(discount)
                    variant.save()
                product.price = product.real_price - float(discount)
                product.save()
            
            offer = Offer(category=category,
                          discount= discount,
                            end_date= end_date,
                
                        )
            offer.save()
            return redirect('offer_management')
    categories=Category.objects.all()
    context={'categories':categories}
    return render(request,'adminside\offers.html',context)


@login_required(login_url='adminside')
def deleteoffer(request,id):
    offer = Offer.objects.get(id=id)
    category = Category.objects.get(id=offer.category.id)
    product_list = Product.objects.filter(category=category)
    for product in product_list:
        variants = SizeVariant.objects.filter(product_id=product)
        for variant in variants:
            variant.price = variant.real_price
            variant.save()
        product.price = product.real_price
        product.save()
    
    
    
    offer.delete()
    messages.warning(request,"Offer deleted Successfully")
    return redirect('offer_management') 


###Offer management side###
###-----End-----###


def graph_chart_management(request):   
    users_count = Profile.objects.count()
    total_users_count =int(users_count - 1 )
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    context = {
        # 'total_order_amount': total_order_amount,
        # 'monthly_totals': monthly_totals,
        'total_users_count':total_users_count,
        'product_count':product_count,
        'category_count':category_count
    }

    return render(request, 'adminside\graph_chart.html', context)


def chart_management(request):
    users_count = Userprofile.objects.count()
    total_users_count =int(users_count + 1 )
    product_count = Product.objects.count()
    order = Order.objects.filter(is_ordered=True).count()
    # for i in monthly_order_totals:
    completed_orders = Order.objects.filter(is_ordered=True)
    
    monthly_totals_dict = defaultdict(float)

    # Iterate over completed orders and calculate monthly totals
    for order in completed_orders:
        order_month = order.created_at.strftime('%m-%Y')
        monthly_totals_dict[order_month] += order.order_total

    months = list(monthly_totals_dict.keys())
    totals = list(monthly_totals_dict.values())

    monthNumber=[]
    totalOrders=[]

            
    variants =SizeVariant.objects.all()
   
    context = {
        'total_users_count':total_users_count,
        'product_count':product_count,
        'order':order,
        # 'orders':orders,
        'variants':variants,
        'months':months,
        'totals':totals,

       
    }
    return render(request,'adminside/chart.html',context)


from collections import defaultdict
from datetime import datetime
# from dateutil.relativedelta import relativedelta

def monthly_order_totals():
    # Get all completed orders
    completed_orders = Order.objects.filter(is_ordered=True)

    # Create a defaultdict to store monthly totals
    monthly_totals_dict = defaultdict(float)

    # Iterate over completed orders and calculate monthly totals
    for order in completed_orders:
        order_month = order.created_at.strftime('%m-%Y')
        monthly_totals_dict[order_month] += order.order_total

    months = list(monthly_totals_dict.keys())
    totals = list(monthly_totals_dict.values())

    return months, totals











