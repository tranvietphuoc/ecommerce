from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddressViewSet,
    ProfileAPIView,
    SendOrResendSMSAPIView,
    UserAPIView,
    UserLoginAPIView,
    UserRegisterationAPIView,
    VerifyPhoneNumberAPIView,
    GoogleLogin,
)

from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

router = DefaultRouter()
router.register(r'', AddressViewSet)


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterationAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('login/google/', GoogleLogin.as_view(), name='google_login'),
    path('send-sms/', SendOrResendSMSAPIView.as_view(), name='send_resend_sms'),
    path(
        'verify-phone/',
        VerifyPhoneNumberAPIView.as_view(),
        name='verify_phone_number',
    ),
    path('', UserAPIView.as_view(), name='user_detail'),
    path('profile/', ProfileAPIView.as_view(), name='profile_detail'),
    path('profile/address/', include(router.urls)),
]
