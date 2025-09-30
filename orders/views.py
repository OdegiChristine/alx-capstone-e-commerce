from rest_framework import generics, permissions, status
from .models import Order, Cart, Wishlist, OrderItem
from .serializers import OrderSerializer, CartSerializer, WishListSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve a list of orders",
        responses={
            200: openapi.Response("List of orders retrieved successfully"),
            401: openapi.Response("Unauthorized"),
        }
    )
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Create a new order",
        request_body=OrderSerializer,
        responses={
            201: openapi.Response("Order created successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
        },
    ),
)
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


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Retrieve a single order by ID",
        responses={
            200: openapi.Response("Order retrieved successfully"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Order not found"),
        },
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Update an order completely",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response("Order updated successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Order not found"),
        },
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Update an order partially",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response("Order updated successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Order not found"),
        },
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description="Delete an order",
        request_body=OrderSerializer,
    ),
)
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


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve a list of carts",
        responses={
            200: openapi.Response("List of cart items retrieved successfully"),
            401: openapi.Response("Unauthorized"),
        }
    )
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Add a new item to cart",
        request_body=OrderSerializer,
        responses={
            201: openapi.Response("Item added successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
        },
    ),
)
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


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Retrieve a cart by id",
        responses={
            200: openapi.Response("Cart retrieved successfully"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Cart not found"),
        },
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Update a cart completely",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response("Cart updated successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Cart not found"),
        },
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Update a cart partially",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response("Cart updated successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Cart not found"),
        },
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description="Delete a cart item",
        request_body=OrderSerializer,
    ),
)
class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()

        return Cart.objects.filter(customer=self.request.user)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve a list of wishlists",
        responses={
            200: openapi.Response("List of wishlists retrieved successfully"),
            401: openapi.Response("Unauthorized"),
        }
    )
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Add a new item to the wishlist",
        request_body=OrderSerializer,
        responses={
            201: openapi.Response("Item added successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
        },
    ),
)
class WishlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Wishlist.objects.none()

        return Wishlist.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Retrieve a wishlist by id",
        responses={
            200: openapi.Response("Wishlist retrieved successfully"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("User not found"),
        },
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Update a wishlist completely",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response("Wishlist updated successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Wishlist not found"),
        },
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Update a wishlist partially",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response("Wishlist updated successfully"),
            400: openapi.Response("Bad request — validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Wishlist not found"),
        },
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description="Delete a wishlist",
        request_body=OrderSerializer,
    ),
)
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

    @swagger_auto_schema(
        operation_description="Checkout a cart",
    )
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

