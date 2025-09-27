from rest_framework import generics, permissions, status
from .models import Order, Cart, Wishlist, OrderItem
from .serializers import OrderSerializer, CartSerializer, WishListSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        if getattr(user, "is_seller", False):
            return Order.objects.filter(items__product__seller=user).distinct()
        else:
            return Order.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        if getattr(user, "is_seller", False):
            return Order.objects.filter(items_product_seller=user).distinct()
        else:
            return Order.objects.filter(customer=user)


class CartListCreateView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all cart items for the authenticated customer.

    post:
    Add a new item to the authenticated customer's cart.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()

        return Cart.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()

        return Cart.objects.filter(customer=self.request.user)


class WishlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Wishlist.objects.none()

        return Wishlist.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class WishlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Empty queryset for docs
        if getattr(self, "swagger_fake_view", False):
            return Wishlist.objects.none()

        return Wishlist.objects.filter(customer=self.request.user)


class CartCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(customer=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(customer=user)

        # Move cart items to order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

        # Clear cart
        cart_items.delete()

        return Response({"message": "Checkout successful", "order_id": order.id}, status=status.HTTP_201_CREATED)

