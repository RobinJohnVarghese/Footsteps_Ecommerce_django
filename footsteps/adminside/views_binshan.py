# import calendar


# @never_cache

# @login_required(login_url="ad_login")
# def ad_home(request):
#     delivered_orders = Orders.objects.filter(status='Delivered')
#     delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
#     print( delivered_orders_by_months)
#     delivered_orders_month = []
#     delivered_orders_number = []
#     for d in delivered_orders_by_months:
#          delivered_orders_month.append(calendar.month_name[d['delivered_month']])
#          delivered_orders_number.append(list(d.values())[1])


#     order_by_months = Orders.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
#     monthNumber = []
#     totalOrders = []
#     for o in order_by_months:
#          monthNumber.append(calendar.month_name[o['month']])
#          totalOrders.append(list(o.values())[1])
#     # print(delivered_orders_number)

#     delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
#     delivered_orders_year = []
#     delivered_orders_year_number = []
#     for d in delivered_orders_by_years:
#         delivered_orders_year.append(d['delivered_year'])
#         delivered_orders_year_number.append(d['delivered_count'])
    
#     order_by_years = Orders.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
#     yearNumber = []
#     totalOrdersYear = []
#     for o in order_by_years:
#         yearNumber.append(o['year'])
#         totalOrdersYear.append(o['count'])
    
#     context ={
#          'delivered_orders':delivered_orders,
#          'order_by_months':order_by_months,
#          'monthNumber':monthNumber,
#          'totalOrders':totalOrders,
#          'delivered_orders_number':delivered_orders_number,
#          'delivered_orders_month':delivered_orders_month,
#          'delivered_orders_by_months':delivered_orders_by_months,
#          'order_by_years': order_by_years,
#          'yearNumber': yearNumber,
#          'totalOrdersYear': totalOrdersYear,
#          'delivered_orders_year': delivered_orders_year,
#          'delivered_orders_year_number': delivered_orders_year_number,
#          'delivered_orders_by_years': delivered_orders_by_years,


#     }

#     return render(request,"admin/ad-home.html",context)

# def sales_report(request):
#     products = Product.objects.all()
#     context = {
#         'products': products
#     }
#     return render(request, 'admin/sales-report.html', context)


# # views.py



# def sales_date(request):
#     if request.method == 'GET':
#         form = DateFilterForm(request.GET)
#         # order_by_date = Orders.objects.annotate(month=ExtractDay('created_at')).values('day').annotate(count=Count('id')).values('day','count')
#         # totalOrders = []
#         # for o in order_by_date:
#         #  totalOrders.append(list(o.values())[1])

#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']

#             # Query the sales data within the specified date range

#             sales_data = Orders.objects.filter(created_at__range=[start_date, end_date]).order_by("-created_at")

#             return render(request, 'admin/sales-report-daily.html', {'sales_data': sales_data, 'form': form,})

#     else:
#         form = DateFilterForm()

#     return render(request, 'admin/sales-report-daily.html', {'form': form})



# def sales_report_by_products(request,id):
#     product = Product.objects.get(pk=id)
#     orders = ProductOrder.objects.filter(product=product)
#     s = product.variant.all()
#     total_stock = 0
#     for s in s:
#       total_stock += s.stock
      
#     delivered_orders = []
#     delivered_quantity = 0
#     for order in orders:
#         if order.order.status == 'Delivered':
#            delivered_orders.append(order)
#            delivered_quantity += order.quantity
    
#     number_delivered_orders = len(delivered_orders)

    
#     context = {
#         'product':product,
#         'orders':orders,
#         'delivered_quantity':delivered_quantity,
#         'number_delivered_orders':number_delivered_orders,
#         'total_stock':total_stock,
#     }
    

#     return render(request, 'admin/sales-report-productwise.html',context)