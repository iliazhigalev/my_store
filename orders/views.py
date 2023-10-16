from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order


class OrderCreateView(TitleMixin, CreateView):
    """ The class places an order for the client """
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'zhigalev_store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderListView(TitleMixin, ListView):
    """ The class shows a page with customer orders """

    template_name = 'orders/orders.html'
    title = 'zhigalev_store - Заказы'
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)
