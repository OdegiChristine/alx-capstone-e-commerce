from django.urls import path
from .views import (
    OrderListCreateView,
    OrderDetailView,
    CartListCreateView,
    CartDetailView,
    WishlistDetailView,
    WishlistListCreateView,
    CartCheckoutView,
)

urlpatterns = [
    #orders
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    # cart
    path("cart/", CartListCreateView.as_view(), name="cart-list-create"),
    path("cart/<int:pk>/", CartDetailView.as_view(), name="cart-detail"),
    path("cart/checkout/", CartCheckoutView.as_view(), name="cart-checkout"),
    #Wishlist
    path("wishlist/", WishlistListCreateView.as_view(), name="wishlist-list-create"),
    path("wishlist/<int:pk>/", WishlistDetailView.as_view(), name="wishlist-detail"),
]
