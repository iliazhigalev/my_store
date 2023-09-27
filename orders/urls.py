from django.urls import path

from orders.views import OrderCreateView,OrderListView

app_name = 'orders'  # название приложения

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),

]
