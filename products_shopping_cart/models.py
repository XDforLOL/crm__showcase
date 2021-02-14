from django.db import models
from crm_retail.models import User


class Products(models.Model):
    product_id = models.IntegerField(primary_key=True, null=False)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    maker = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    created_on = models.DateTimeField('created_on', auto_now_add=True)

    class Meta:
        db_table = 'products'
        managed = True

    def __str__(self):
        return f"{self.product_name}"
