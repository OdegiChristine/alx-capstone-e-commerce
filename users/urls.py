from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import CustomerRegisterView, UserDeleteView, UserProfileRetrieveUpdateView, SellerRegisterView

urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view(), name='register-customer'),
    path('register/seller/', SellerRegisterView.as_view(), name='register-seller'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete/', UserDeleteView.as_view(), name='delete-account'),
    path('profile/', UserProfileRetrieveUpdateView.as_view(), name='profile'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
