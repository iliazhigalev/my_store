from django.urls import path

from .views import (ProductDetailView, ProductsListView, add_basket,
                    basket_remove)

app_name = 'products'  # название приложения

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    #path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('detail_product/<int:pk>/', ProductDetailView.as_view(), name='product_detail_view'),
    path('baskets/add/<int:product_id>/', add_basket, name='add_basket'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
