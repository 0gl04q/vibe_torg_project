from django.contrib import admin

from apps.orders.models import Order, Buyer


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    pass
