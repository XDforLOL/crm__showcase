# for sale_detail in sale_details:
#     sale_details_instance_form = SaleDetailsForm(instance=sale_detail)
#     list_of_sale_details_forms.append(sale_details_instance_form)
#    # sale_detail = SaleDetails.objects.get(sale=sale_id)


#     # dict(request.POST.items())
#     sales_form = SalesForm(request.POST, instance=sale)
#     for index, sale_detail_form in enumerate(list_of_sale_details_forms):
#         for sale_detail in sale_details:
#             list_of_sale_details_forms[index] = SaleDetailsForm(request.POST, instance=sale_detail)

# sale_details_instance_form = SaleDetailsForm(request.POST,instance=sale_detail)
# list_of_sale_details_forms.append(sale_details_instance_form)
# list_of_sale_details_forms = SaleDetailsForm(request.POST, instance=sale_detail)
# = [sale_detail_form.SaleDetailsForm(request.POST, instance=sale_detail)
#                               for sale_detail_form
#                               in list_of_sale_details_forms]
# for sale_detail_form in list_of_sale_details_forms:
#     sale_detail_form = SaleDetailsForm(request.POST, instance=sale_detail)



# sales_details = SaleDetails.objects.select_related('sale').all()
# current_customer_sale_detail.append(sales_details)
#     prefetched_sale_details = Sales.objects.prefetch_related('saledeatils_set').get(sale_id=sale)
#     current_customer_sale_detail = [sale_detail for sale_detail in sales_details.filter(sale_id=sale)]


# product_id = ''

# {product_id: {'sale_detail': get_id(SaleDetails, 'sale_detail'),
#               'id': id,
#               'quantity': quantity,
#               'sale': sale_id}}

# if request.method == 'POST':
#     sale_details_form = SaleDetailsForm(data={
#         'product': ,
#         'quantity': ,
#     })
# product_quantity = [q.get('quantity') for q in cart.values()]
# cart_product_ids = cart.keys()
#
#
#
# for product, quantity in cart_product_ids, product_quantity:
#     # for form in sale_details_form:
#     s_d_f = sale_details_form(data={
#         'sale_detail': get_id(SaleDetails, 'sale_detail'),
#         'product': product,
#         'quantity': quantity,
#         'sale': sale_id
#     })

# if s_d_f.is_valid():
#     s_d_f.save()


# def product_detail(request: HttpRequest, id: str, slug):
#     product = get_object_or_404(Products, product_id=id,
#                                 slug=slug,
#                                 available=True)
#
#     cart_product_form = CartAddProductForm()
#
#     return render(request,
#                   'shopping_cart/products/product_detail.html',
#                   {
#                       'product': product,
#                       'cart_product_form': cart_product_form
#                   })