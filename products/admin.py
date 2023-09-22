from django.contrib import admin

from .models import *

admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')#как мы видим поле на главной странице в админке,с какими полями, что отображать
    fields = ('name','description',('price','quantity'),'category','image')
    search_fields = ('name',)#поиск по имени в админке


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'price', 'created_timestamp', 'quantity')
    readonly_fields = ('created_timestamp', 'price')
    extra = 0

    def price(self, instance):
        try:
            return instance.product.price
        except models.Product.DoesNotExist:
            return 'Unknown'