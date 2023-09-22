from django.contrib import admin

from products.admin import BasketAdmin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email')#как мы видим поле на главной странице в админке,с какими полями, что отображать
    inlines = (BasketAdmin,)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code','user','expiration')
    fields = ('code','user','expiration','created',)
    readonly_fields = ('created',)