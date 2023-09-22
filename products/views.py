from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = "zhigalev_store - Главная"


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    title = 'zhigalev_store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')  # берём id категории
        return queryset.filter(category_id=category_id) if category_id else queryset

class ProductDetailView(TitleMixin,DetailView):
    model = Product
    template_name = 'products/product.html'
    title = 'zhigalev_store '
    context_object_name = 'product'


@login_required
def add_basket(request, product_id: int):
    product = Product.objects.get(id=product_id)
    baskets_items = Basket.objects.filter(user=request.user,
                                          product=product).first()  # беру корзину пользователя с определёным продуктом

    if not baskets_items:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets_items.quantity += 1
        baskets_items.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # верну ту страницу на которой находится пользователь


@login_required
def basket_remove(request, basket_id: int):
    basket_id = Basket.objects.get(id=basket_id)
    basket_id.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # верну ту страницу на которой находится пользователь


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
