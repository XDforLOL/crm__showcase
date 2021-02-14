import psycopg2

from .models import Products
from datetime import datetime
from django_retail_crm.secret_key import host, psql_key
from django.forms import modelformset_factory
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from crm_retail.views import get_id
from crm_retail.models import Sales, SaleDetails
from crm_retail.forms import SalesForm, SaleDetailsForm
from crm_retail.decorators import unauthorized_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from .cart_form import CartAddProductForm




@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request: HttpRequest, product_id: str):
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def product_detail(request: HttpRequest, id: str, slug):
    product = get_object_or_404(Products, product_id=id,
                                slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    return render(request,
                  'shopping_cart/products/product_detail.html',
                  {
                      'product': product,
                      'cart_product_form': cart_product_form
                  })


def cart_detail(request: HttpRequest):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    return render(request, 'shopping_cart/cart/detail.html', {'cart': cart})


def products(request: HttpRequest) -> HttpResponse:
    return render(request, 'shopping_cart/products/products.html',
                  {'products': Products.objects.all(),
                   'cart_product_form': CartAddProductForm()})


def check_out(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        conn = psycopg2.connect(
            host=host,
            database="retaildb",
            user="postgres",
            password=psql_key)
        cur = conn.cursor()

        sale_id = get_id(Sales, 'sale_id')
        customer_id = request.user.id
        sales_form = SalesForm(data={
            'sale_id': sale_id,
            'customer_id': customer_id,
            'status': 'Pending'
        })
        if sales_form.is_valid():
            sales_form.save()

        for item in Cart(request).cart.items():
            item_id, item_props = item
            query = f"""
            INSERT INTO public.sale_details(sale_detail, quantity, created_on, product_id, sale_id) 
            VALUES ({get_id(SaleDetails, 'sale_detail')},
            {item_props['quantity']}, 
            '{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}', 
            {item_id}, {sale_id})
            """
            cur.execute(query)
            conn.commit()
            print(query)
    del Cart(request).cart
    context = {}
    return render(request, 'shopping_cart/cart/checkout.html', {'context': context})

# TODO finish checkout register sales properly
# TODO when registering a new a account fix check button
# TODO Touchup the customer filter to display messages properly and pretty
# TODO touchup products page to have a rulleta for items
# TODO limit Sales and customers dashboard to 5 items all the time with option to load next maybe
