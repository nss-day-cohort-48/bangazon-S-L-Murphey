from django.urls import path
from .views import product_price_list

urlpatterns = [
    path('reports/productprice', product_price_list),
]