from django.db import models

from users.models import User

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'  # название в админ панели


class Product(models.Model):
    class Meta:
        verbose_name_plural = 'Товары в магазине'  # название в админ панели

    name = models.CharField(max_length=256, unique=True, verbose_name='Имя товара')
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")  # цена
    quantity = models.PositiveIntegerField(default=0)  # количество товара на складе
    image = models.ImageField(upload_to='products_images', verbose_name="Фото")
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    class Meta:
        verbose_name_plural = 'Корзина товаров'  # название в админ панели

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Корзина пользователя")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар в корзине")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество добавленных товаров в корзину")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления в корзину")

    objects = BasketQuerySet.as_manager()  # использую BasketQuerySet,как менеджера

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
