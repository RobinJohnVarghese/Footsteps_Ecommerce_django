# def inc_cart_item(request, item_id):
#     item = CartItems.objects.get(id=item_id)
#     size = SizeVariant.objects.get(uid=item.product_variant.uid)
#     total = 0
#     quantity = 0
#     try:
#         cart_items = CartItems.objects.filter(user=request.user, is_active=True)
#         total_existing = CartItems.objects.filter(user=request.user, is_active=True).aggregate(total_quantity=Sum('quantity'))[
#             'total_quantity']
#     except:
#         cart = uCart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItems.objects.filter(cart=cart, is_active=True)

#         total_existing = CartItems.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))[
#             'total_quantity']

#     if total_existing is None:
#         total_existing = 0
#     if total_existing>=10:
#         # messages.info(request, 'You can Only Put 10 items to Cart at a time')
#         for cart_item in cart_items:
#             total += (cart_item.product_variant.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total) / 100
#         grant_total = total + tax


#         return JsonResponse({
#             'price': item.product_variant.price,
#             'quantity': item.quantity,
#             'total': total,
#             'grant_total': grant_total,
#             'tax': tax,
#             'total_existing': total_existing,
#         })

#     if size.stock >= 1:
#         size.stock -= 1
#         size.save()
#         item.quantity += 1
#         item.save()

#         for cart_item in cart_items:
#             total += (cart_item.product_variant.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total) / 100
#         grant_total = total + tax

#         print("total_existing =================== ",total_existing)

#         return JsonResponse({
#             'price': item.product_variant.price,
#             'quantity': item.quantity,
#             'total': total,
#             'grant_total': grant_total,
#             'tax': tax,
#             'total_existing': total_existing,
#         })
#     else:
#         return JsonResponse({'error': 'Product out of Stock'})
 
# def dec_cart_item(request, item_id):
#     item = CartItems.objects.get(id=item_id)
#     size = SizeVariant.objects.get(uid=item.product_variant.uid)

#     total = 0
#     quantity = 0
#     total_existing = 0
#     try:
#         cart_items = CartItems.objects.filter(user=request.user, is_active=True)
#     except:
#         cart = uCart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItems.objects.filter(cart=cart, is_active=True)

#     # cart_items = CartItems.objects.filter(user=request.user, is_active=True)
#     if item.quantity > 1:
#         size.stock += 1
#         size.save()
#         item.quantity -= 1
#         item.save()
#         for cart_item in cart_items:
#             total += (cart_item.product_variant.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total) / 100
#         grant_total = total + tax


#         return JsonResponse({
#             'price':item.product_variant.price,
#             'quantity': item.quantity,
#             'total': total,
#             'grant_total': grant_total,
#             'tax': tax,

#         })
#     else:
#         size.stock += 1
#         size.save()
#         item.delete()
#         return JsonResponse({'removed': True})