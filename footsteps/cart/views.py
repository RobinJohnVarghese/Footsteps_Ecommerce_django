from django.shortcuts import render,redirect,get_object_or_404
from adminside.models import *
from ecommerce.models import *
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Cart
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return redirect('cart')

from django.db.models import Sum
def add_cart(request,product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        size_id = request.POST.get('size_id')
        color_id = request.POST.get('color_id')
        quantity = 1
        if request.user.is_authenticated:
            total_items = CartItem.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            if total_items is None:
                total_items = 0
            if total_items > 10:
                messages.warning(request, f'Cart Limit Reached You already have {total_items} in Your cart and you can add {10-total_items} items')
                return redirect('product_details', product_id=product_id)
            if size_id and color_id:
                product = Product.objects.get(id=product_id)
                
                color = ColorVariant.objects.get(id=color_id)
                try:
                    variant = SizeVariant.objects.get(size=size_id, Color_id=color)
                except:
                    messages.warning(request, "This Color does not have this Size, Please Select another.")
                    return redirect('product_details', product_id)
                try:
                    total_items = CartItem.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))[
                        'total_quantity']
                    if total_items is None:
                        total_items = 0
                    if total_items + quantity > 10:
                        messages.warning(request,
                                         f'Cart Limit Reached You already have {total_items} items '
                                         f'in Your cart and you can add {10 - total_items} items')
                        return redirect('product_details', product_id=product_id)
                    cart_item = CartItem.objects.get(variations=variant, user=request.user)
                    if variant.stock > quantity:
                        variant.stock -= quantity
                        cart_item.quantity += quantity
                        cart_item.save()
                        # variant.save()
                        messages.success(request, 'Product Added to cart ')
                        return redirect('product_details', product_id=product_id)
                    else:
                        messages.info(request, 'Product Out of stock ')
                        return redirect('product_details', product_id=product_id)
                except CartItem.DoesNotExist:
                    if variant.stock >= quantity:
                        variant.stock -= quantity
                        cart_item = CartItem.objects.create(product=product,
                                                             quantity=quantity,
                                                             user=request.user,
                                                             variations=variant)
                        cart_item.save()
                    else:
                        messages.info(request, 'Product Out of stock')
                        return redirect('product_details', product_id=product_id)
                return redirect('cart')
            else:
                messages.error(request, 'Please Select a Color and Size')
                return redirect('product_details', product_id=product_id)
        else:
            if size_id:
                product = Product.objects.get(id=product_id)
                variant = SizeVariant.objects.get(id=size_id)
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()
                total_items = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity']
                if total_items is None:
                    total_items = 0
                if total_items > 10:
                    messages.warning(request,
                        f'Cart Limit Reached You already have {total_items} in Your cart and you can add {10 - total_items} items')
                    return redirect('product_details', product_id=product_id)
                try:
                    total_items = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))[
                        'total_quantity']
                    if total_items is None:
                        total_items = 0
                    if total_items+quantity > 10:
                        messages.warning(request,
                                         f'Cart Limit Reached You already have {total_items} items '
                                         f'in Your cart and you can add {10 - total_items} items')
                        return redirect('product_details', product_id=product_id)
                    cart_item = CartItem.objects.get(variations=variant, cart=cart)
                    if variant.stock > quantity:
                        variant.stock -= quantity
                        cart_item.quantity += quantity
                        cart_item.save()
                    else:
                        messages.info(request, 'Product Out of stock ')
                        return redirect('product_details', product_id=product_id)
                except CartItem.DoesNotExist:
                    if variant.stock > quantity:
                        variant.stock -= quantity
                        cart_item = CartItem.objects.create(product=product,
                                                             quantity=quantity,
                                                             cart=cart,
                                                             variations=variant)
                        cart_item.save()
                    else:
                        messages.info(request, 'Product Out of stock  ')
                        messages.error(request, 'Please Select a Color and Size')
            else:
                messages.error(request,'Please Select a Color and Size')
                return redirect('product_details', product_id=product_id)

            messages.success(request, 'Product Added to Cart')
            return redirect('product_details', product_id=product_id)



def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(user=request.user)
            print("logged")
        else:
            print("notlogged")
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_items = CartItem.objects.filter(cart=cart)
        if cart_item.quantity > 1:
            variant = cart_item.variations
            cart_item.quantity -= 1
            cart_item.save()
            tax = 0
            grand_total = 0
            total = 0
            
            for cart_itm in cart_items:
                total += (cart_itm.variations.price * cart_itm.quantity)
            tax = (2 * total)/100
            grand_total = total + tax
            return JsonResponse({
            'price':cart_item.variations.price,
            'total': total,
            'quantity': cart_item.quantity,
            'tax'       : tax,
            'grand_total': grand_total,
            })
        else: 
            variant = cart_item.variations
            variant.stock += 1
            cart_item.delete()
            return JsonResponse({'removed':True})
    except:
        pass
    return redirect('cart')



def inc_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
            cart_items = CartItem.objects.filter(cart=cart)
        if cart_item.variations.stock >0:
            variant = cart_item.variations
            if cart_item.quantity >= 1:
                cart_item.quantity += 1
                cart_item.save()
        else:
            messages.warning(request, 'Out of Stock')
            return JsonResponse({'outofstock':True})
    except:
        pass
    tax = 0
    grand_total = 0
    total = 0
    for cart_itm in cart_items:
        total += (cart_itm.variations.price * cart_itm.quantity)
    tax = (2 * total)/100
    grand_total = total + tax
    
    return JsonResponse({
        'price':cart_item.variations.price,
        'total': total,
        'quantity': cart_item.quantity,
        # 'cart_items': cart_item,
        'tax'       : tax,
        'grand_total': grand_total,
        })

        

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)  
    cart_item.delete()
    return redirect('cart')


            
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.variations.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        applied_coupon = request.session.get('coupon_applied', None)
        if applied_coupon:
            try:
                coupon = Coupon.objects.get(coupon_code=applied_coupon, is_expired=False, minimum_amount__lte=total)
                total -= coupon.discount_price
                grand_total = total + tax
            except Coupon.DoesNotExist:
                # Handle the case where the coupon does not exist or does not meet the minimum amount criteria
                pass
    except ObjectDoesNotExist:
        pass #just ignore
    context = {
       'applied_coupon': applied_coupon,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'ecommerce/shop-cart.html',context)


@login_required(login_url='signin')
def checkout(request, total=0, quantity=0, cart_items=None):
    variants=SizeVariant.objects.filter()
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.variations.price * cart_item.quantity)
            quantity += cart_item.quantity
            if cart_item.quantity > cart_item.variations.stock:
                messages.info(request , f'{cart_item.variations.product_id.product_name} is in out of stock')
                return redirect('cart')
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    current_user = request.user
    user1 = Userprofile.objects.get(user=current_user)
    address = Profile.objects.filter(user=user1)
    try:
        ad = address.get(user=user1,is_default=True)
    except:
        ad = None
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'address':address,
        'user1':user1,
        'ad':ad,
    }
    return render(request, 'ecommerce/checkout.html', context)

def select_address(request,address_id):
    userpro = Userprofile.objects.get(user=request.user)
    address_l = Profile.objects.filter(user=userpro)
    if len(address_l) == 1:
        messages.info(request , 'Only One Address is Present, You Can not Unselect this')
        return redirect('checkout')
    address = Profile.objects.get(id=address_id)
    address.is_default=True
    address.save()
    address_list = Profile.objects.filter(user=userpro).exclude(id=address_id)
    for ad in address_list:
        ad.is_default = False
        ad.save()
    return redirect('checkout')
               
    
def get_cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.cartitem_set.count()
            return JsonResponse({'cart_count': cart_count})
    return JsonResponse({'cart_count': 0})



