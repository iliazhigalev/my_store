from django.db import models
from users.models import User
from typing import Tuple


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name_plural: str = 'Категории'  # Name in the admin panel


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='Имя товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0)  # Quantity of goods in stock
    image = models.ImageField(upload_to='products_images', verbose_name='Фото')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категории')

    def __str__(self) -> str:
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    class Meta:
        verbose_name_plural: str = 'Товары в магазине'


class BasketQuerySet(models.QuerySet):

    def total_sum(self) -> int:
        return sum(basket.sum() for basket in self)

    def total_quantity(self) -> int:
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Корзина пользователя')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар в корзине')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество добавленных товаров в корзину')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления в корзину')
    objects = BasketQuerySet.as_manager()  # I use BasketQuerySet as a manager

    def __str__(self) -> str:
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self) -> int:
        return self.product.price * self.quantity

    class Meta:
        verbose_name_plural: str = 'Корзина товаров'  # Name in the admin panel

    @classmethod
    def create_or_update(cls, product_id: int, user) -> Tuple:
        product = Product.objects.get(id=product_id)
        baskets_items = Basket.objects.filter(user=user,
                                              product=product).first()  # I take the user's cart with a certain product

        if not baskets_items:
            obj = Basket.objects.create(user=user, product=product, quantity=1)
            is_created = True
            return obj, is_created
        else:
            baskets_items.quantity += 1
            baskets_items.save()
            is_created = False
            return baskets_items, is_created
