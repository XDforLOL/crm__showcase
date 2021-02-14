from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('checkout/', views.check_out, name='checkout'),
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^cart_add/(?P<product_id>\d+)/$',
        views.cart_add,
        name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$',
        views.cart_remove,
        name='cart_remove'),
]
