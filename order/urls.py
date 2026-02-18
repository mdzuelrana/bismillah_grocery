from rest_framework.routers import DefaultRouter
from .views import SellerOrderViewSet,OrderViewSet

router = DefaultRouter()
router.register('seller-orders', SellerOrderViewSet, basename='seller-orders')
router.register('seller-orders_create', OrderViewSet, basename='seller-orders_create')

urlpatterns = router.urls
