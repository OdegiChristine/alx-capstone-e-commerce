from rest_framework import serializers
from .models import Order, OrderItem, Cart, Wishlist


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "created_at", "items"]
        read_only_fields = ["customer", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "product", "quantity"]


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["id", "product"]
