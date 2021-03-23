import psycopg2
import os
from .models import Products
from datetime import datetime
from django_retail_crm.secret_key import host, psql_key
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from crm_retail.views import get_id
from crm_retail.models import Sales, SaleDetails
from crm_retail.forms import SalesForm
from django.views.decorators.http import require_POST
from .cart import Cart
from .cart_form import CartAddProductForm


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add_product_to_cart(product=product,
                                 quantity=cd['quantity'],
                                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    cart.remove_product_from_cart(product)
    return redirect('cart:cart_detail')


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    return render(request, 'shopping_cart/cart/detail.html', {
        'cart': cart,
        'total_cart': [sum(i['quantity'] for i in Cart(request).cart.values())][0]
    })


def products(request: HttpRequest) -> HttpResponse:
    return render(request, 'shopping_cart/products/products.html',
                  {'products': Products.objects.all(),
                   'cart_product_form': CartAddProductForm(),
                   'total_cart': [sum(i['quantity'] for i in Cart(request).cart.values())][0]
                   })


def products_detail(request) -> HttpResponse:
    return render(request, 'shopping_cart/products/product_detail.html', {'products': Products.objects.all()})


def check_out(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_SECRET')
        )
        cur = conn.cursor()

        sale_id = get_id(Sales, 'sale_id')
        customer_id = request.user.customers.pk
        sales_form = SalesForm(data={
            'sale_id': sale_id,
            'customer_id': customer_id,
            'time_of_order': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
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
            Cart(request).clear()
    return redirect('cart:cart_detail')

# TODO finish checkout register sales properly
# TODO when registering a new a account fix check button
# TODO Touchup the customer filter to display messages properly and pretty
# TODO touchup products page to have a rulleta for items
# TODO limit Sales and customers dashboard to 5 items all the time with option to load next maybe
