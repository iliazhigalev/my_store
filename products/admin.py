from django.contrib import admin
from .models import *

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',
                    'category')  # How do we see the field on the main page of the page in the admin panel
    fields = ('name', 'description', ('price', 'quantity'), 'category', 'image')
    search_fields = ('name',)  # Search by name in the admin panel


class BasketAdmin(admin.TabularInline):
    """ the class is responsible for displaying the basket of goods in the admin area """
    model = Basket
    fields = ('product', 'price', 'created_timestamp', 'quantity')
    readonly_fields = ('created_timestamp', 'price')
    extra = 0

    def price(self, instance):
        try:
            return instance.product.price
        except models.Product.DoesNotExist:
            return 'Unknown'
