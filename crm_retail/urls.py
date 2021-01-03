from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main'),
    path('products/', views.products, name="products"),
    path('customers/<str:customer_id>/', views.customers, name="customers"),
    path('profile', views.customer_profile, name='profile'),
    path('profile_setting', views.profile_setting, name='profile_settings'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),

    path('create_sale/<str:customer_id>', views.create_sale, name='create_sale'),
    path('update_sale/<str:sale_id>', views.update_sale, name='update_sale'),
    path('delete_sale/<str:sale_id>', views.delete_sale, name='delete_sale')
]
