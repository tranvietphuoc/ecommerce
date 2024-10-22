"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import GoogleLogin


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls", namespace="users")),
    path("api/products/", include("products.urls", namespace="products")),
    path("api/users/orders/", include("orders.urls", namespace="orders")),
    path("api/users/payment/", include("payment.urls", namespace="payment")),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path(
        "api/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account-confirm-email",
    ),
    path(
        "account-email-verification-sent/",
        TemplateView.as_view(),
        name="account-email-verification-sent",
    ),
    path("users/login/google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Schema URLs
urlpatterns += [
    path(
        "api/schema/",
        SpectacularAPIView.as_view(api_version="1.0"),
        name="schema",
    ),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
