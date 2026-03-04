"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from tasks.views import ProductViewSet, CategoryViewSet
from cart.views import CartItemViewSet, WishlistViewSet
from order.views import OrderViewSet,AdminOrderViewSet
from review.views import ReviewViewSet
from users.views import AdminProductViewSet,AdminDashboardStats,ProfileView
schema_view = get_schema_view(
   openapi.Info(
      title="grocery",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register('products', ProductViewSet,basename='products')
router.register('categories', CategoryViewSet,basename='categories')
router.register('cart', CartItemViewSet,basename='carts')
router.register('wishlist', WishlistViewSet,basename='wishlists')
router.register('orders', OrderViewSet,basename='orders')
router.register('reviews', ReviewViewSet,basename='reviews')
router.register('admin-products', AdminProductViewSet, basename='admin-products')
router.register('admin-orders', AdminOrderViewSet, basename='admin-orders')
urlpatterns = [
    path('api/payment/', include('payments.urls')),
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += [
    path('api/admin-dashboard/', AdminDashboardStats.as_view()),
    path('api/profile/', ProfileView.as_view()),
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)