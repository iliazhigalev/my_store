from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.urls import reverse_lazy
from common.views import TitleMixin
from django.views.generic.list import ListView
from orders.models import Order


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'zhigalev_store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'zhigalev_store - Заказы'
    queryset = Order.objects.all()


    def get_queryset(self):
        queryset = super(OrderListView,self).get_queryset()
        return queryset.filter(initiator=self.request.user)
