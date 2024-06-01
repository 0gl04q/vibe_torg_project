from rest_framework import serializers

from apps.orders.models import Order, Buyer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'buyer', 'link', 'price', 'status')


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ('tg_id', 'nickname')
