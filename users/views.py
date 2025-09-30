from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

User = get_user_model()


class BaseRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    role = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.role == "seller":
            user = serializer.save(is_customer=False, is_seller=True)
        else:
            user = serializer.save(is_customer=True, is_seller=False)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class CustomerRegisterView(BaseRegisterView):
    role = "customer"

    @swagger_auto_schema(
        operation_description="Register as a customer",
        responses={201: openapi.Response("Customer registered successfully")}
    )
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SellerRegisterView(BaseRegisterView):
    role = "seller"

    @swagger_auto_schema(
        operation_description="Register as a seller",
        responses={201: openapi.Response("Seller registered successfully")}
    )
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete user account",
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile",
        responses={200: openapi.Response("User profile retrieved successfully")}
    )
)
class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
