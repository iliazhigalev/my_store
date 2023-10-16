from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from .models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_index(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'zhigalev_store - Главная')
        self.assertEqual(response.template_name, ['products/index.html'])


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']), list(self.products.filter(category=category.id))
        )

    def _common_tests(self, response):
        self.assertEqual(response.template_name[0], 'products/products.html')
        self.assertEqual(response.context_data['title'], 'zhigalev_store - Каталог')
        self.assertEqual(response.status_code, HTTPStatus.OK)
