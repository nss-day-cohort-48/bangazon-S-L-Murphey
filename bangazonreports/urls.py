from django.urls import path
from .views import product_price_list
from .views import inexpensive_product_list

urlpatterns = [
    path('reports/productprice', product_price_list),
    path('reports/inexpensiveproducts', inexpensive_product_list),
]