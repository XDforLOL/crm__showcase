from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.conf import settings
# Create your models here.


class Customers(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField('created_on', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Products(models.Model):
    product_id = models.IntegerField(primary_key=True, null=False)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    maker = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    created_on = models.DateTimeField('created_on', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'products'

    def __str__(self):
        return f"{self.product_name}"


class Sales(models.Model):
    _status = [('Pending', 'Pending'),
               ('Out for delivery', 'Out for delivery'),
               ('Delivered', 'Delivered')]
    sale_id = models.IntegerField(primary_key=True, null=False)
    customer_id = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, null=False)
    time_of_order = models.CharField('ordered_on', max_length=255, blank=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=_status)
    created_on = models.DateTimeField('created_on', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'sales'

    def __str__(self):
        return str(self.sale_id)


class SaleDetails(models.Model):
    sale_detail = models.IntegerField(primary_key=True, null=False)
    sale = models.ForeignKey(Sales, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField('quantity', blank=True, null=True)
    created_on = models.DateTimeField('created_on', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'sale_details'

    def __str__(self):
        return f"sale: {str(self.sale)},product: {str(self.product)}," \
               f"quantity: {str(self.quantity)},created_on: {str(self.created_on)}"

    # , self.product, self.quantity, self.created_on