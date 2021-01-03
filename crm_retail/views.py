from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import SalesForm, CreateUserForm, CustomerForm
from .filters import SalesFilter
from .decorators import unauthorized_user, allowed_users, admin_only


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request: HttpRequest) -> HttpResponse:
    sales = Sales.objects.all()

    return render(
        request,
        'crm_retail/dashboard.html',
        {'sales': sales,
         'customers': Customers.objects.all(),
         'total_orders': sales.count(),
         'orders_delivered': sales.filter(status='Delivered').count(),
         'orders_pending': sales.filter(status='Pending').count()
         }
    )


@unauthorized_user
def register_page(request: HttpRequest) -> HttpResponse:
    pk_last_customer = getattr(Customers.objects.latest('customer_id'), 'pk') + 1
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # TODO Create Logger
        print(form.errors)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customers.objects.create(
                customer_id=pk_last_customer,
                user=user, first_name=user.first_name,
                last_name=user.last_name, mail=user.email,
            )

            messages.success(request, f'Account was created for {username}')
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'crm_retail/customer_registration.html', {'form': form})


@unauthorized_user
def login_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password')
                            )
        if user is not None:
            login(request, user)
            return redirect('profile')

        else:
            messages.info(request, 'Username Or Password Is Incorrect')
            return redirect('login')

    return render(request, 'crm_retail/customer_login.html', {})


def logout_page(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_profile(request: HttpRequest) -> HttpResponse:
    user_customer_orders = request.user.customers.sales_set.all()
    print(f'ORDERS: {user_customer_orders}')
    return render(request,
                  'crm_retail/customer_profile.html',
                  {'user_customer_orders': user_customer_orders,
                   'orders_pending': user_customer_orders.filter(status='Pending').count(),
                   'orders_delivering': user_customer_orders.filter(status='Out for delivery').count(),
                   'orders_delivered': user_customer_orders.filter(status='Delivered').count(),
                   })


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profile_setting(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=request.user.customers)
        if form.is_valid():
            form.save()
    else:
        form = CustomerForm(instance=request.user.customers)
    return render(request, 'crm_retail/profile_settings.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request: HttpRequest, customer_id: str) -> HttpResponse:
    customer = Customers.objects.get(customer_id=customer_id)
    sales = customer.sales_set.all()
    sales_count = sales.count()
    current_customer_sale_detail = {}
    my_filter = SalesFilter(request.GET, queryset=sales)
    sales = my_filter.qs

    for sale in sales:
        current_customer_sale_detail.update({sale: SaleDetails.objects.all().filter(sale_id=sale)})

    return render(request,
                  'crm_retail/customers.html',
                  {'customer': customer, 'sales': sales,
                   'current_customer_sale_detail': current_customer_sale_detail,
                   'sales_count': sales_count, 'my_filter': my_filter
                   })


def products(request: HttpRequest) -> HttpResponse:
    return render(request, 'crm_retail/products.html', {'products': Products.objects.all()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_sale(request: HttpRequest, customer_id: str) -> HttpResponse:
    latest_sale_id = getattr(Sales.objects.latest('sale_id'), 'pk') + 1
    sales_form = SalesForm(initial={
        'sale_id': latest_sale_id, 'customer_id': customer_id})

    sales_form.fields['sale_id'].disabled = True
    sales_form.fields['customer_id'].disabled = True

    sale_details_form_set = modelformset_factory(
        SaleDetails, fields=('product', 'quantity'), can_delete=True, extra=1, max_num=10)
    sale_detail_form_set = sale_details_form_set(queryset=SaleDetails.objects.none())
    if request.method == 'POST':
        POST = request.POST.copy()
        POST['customer_id'] = customer_id
        POST['sale_id'] = latest_sale_id
        sale_detail_form_set = sale_details_form_set(request.POST)
        sales_form = SalesForm(POST)
        if sales_form.is_valid() and sale_detail_form_set.is_valid():
            sales_form.save()
            detail_form = sale_detail_form_set.save(commit=False)

            for obj in sale_detail_form_set.deleted_objects:
                obj.delete()

            for form in detail_form:
                form.sale_id = latest_sale_id
                form.sale_detail = (getattr(
                    SaleDetails.objects.latest('sale_detail'), 'pk') + 1)
                form.save()
            return redirect('/')

    return render(
        request,
        'crm_retail/sales_form.html',
        {'sales_form': sales_form,
         'sale_detail_form_set': sale_detail_form_set
         })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_sale(request: HttpRequest, sale_id: str) -> HttpResponse:
    sale = Sales.objects.get(sale_id=sale_id)
    sale_details_id = SaleDetails.objects.all().filter(sale_id=sale_id)

    sale_details_form_set = modelformset_factory(
        SaleDetails, fields=('product', 'quantity'), can_delete=True, extra=1, max_num=10)

    sale_detail_form_set = sale_details_form_set(
        initial=[{'sale_id': sale_id, 'sale_detail': sale_detail_id.sale_detail}
                 for sale_detail_id in sale_details_id], queryset=sale_details_id
    )

    if request.method == 'POST':
        sales_form = SalesForm(request.POST, instance=sale)
        sale_detail_form_set = sale_details_form_set(request.POST, queryset=sale_details_id)
        if sales_form.is_valid() and sale_detail_form_set.is_valid():
            sales_form.save()
            detail_form = sale_detail_form_set.save(commit=False)

            for obj in sale_detail_form_set.deleted_objects:
                obj.delete()

            for form in detail_form:
                form.instance = sale_details_id
                form.sale_id = sale_id
                form.sale_detail = (getattr(
                    SaleDetails.objects.latest('sale_detail'), 'pk') + 1)
                form.save()
            return redirect('/')
    else:
        sales_form = SalesForm(instance=sale)

    return render(
        request,
        'crm_retail/sales_form.html',
        {'sales_form': sales_form,
         'sale_detail_form_set': sale_detail_form_set
         })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_sale(request: HttpRequest, sale_id: str) -> HttpResponse:
    if request.method == 'POST':
        SaleDetails.objects.all().filter(sale_id=sale_id).delete()
        Sales.objects.get(sale_id=sale_id).delete()
        return redirect('/')
    return render(
        request, 'crm_retail/delete.html', {'item': sale_id})
