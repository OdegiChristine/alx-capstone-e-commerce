from rest_framework import generics, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsSellerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description="Create a category for products",
        request_body=CategorySerializer,
        responses={
            201: openapi.Response("Category created successfully"),
            403: openapi.Response("User not permitted"),
            400: openapi.Response("Bad request"),
        }
    )
)
@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve a list of categories",
        responses={
            200: openapi.Response("List of categories retrieved successfully"),
            401: openapi.Response("Unauthorized")
        }
    )
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSellerOrReadOnly]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve category by id",
        responses={
            200: openapi.Response("Category retrieved successfully"),
            404: openapi.Response("Category not found"),
            401: openapi.Response("Unauthorized"),
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_description="Update a category completely",
        request_body=CategorySerializer,
        responses={
            200: openapi.Response("Category updated successfully"),
            400: openapi.Response("Bad request"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Category not found"),
        }
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_description="Partially update a category",
        request_body=CategorySerializer,
        responses={
            200: openapi.Response("Category updated successfully"),
            400: openapi.Response("Bad request - validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Category not found"),
        }
    )
)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSellerOrReadOnly]


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={
            201: openapi.Response("Product created successfully"),
            400: openapi.Response("Bad request - validation error"),
            401: openapi.Response("Unauthorized"),
        }
    )
)
@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve a list of products",
        responses={
            200: openapi.Response("List of products retrieved successfully"),
            401: openapi.Response("Unauthorized")
        }
    )
)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category"] # Filter by category id
    search_fields = ["name", "description"] # Search by name or description
    ordering_fields = ["price", "created_at"]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve a product by id",
        responses={
            200: openapi.Response("Product retrieved successfully"),
            404: openapi.Response("Product not found")
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_description="Update a product completely",
        request_body=CategorySerializer,
        responses={
            200: openapi.Response("Product updated successfully"),
            400: openapi.Response("Bad request"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Product not found"),
        }
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_description="Partially update a product",
        request_body=CategorySerializer,
        responses={
            200: openapi.Response("Product updated successfully"),
            400: openapi.Response("Bad request - validation error"),
            401: openapi.Response("Unauthorized"),
            404: openapi.Response("Product not found"),
        }
    )
)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]
