from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('categories', views.CategoryViewSet)
router.register('unit-measurements', views.UnitMeasurementViewSet)
router.register('suppliers', views.SupplierViewSet)
router.register('customers', views.CustomerViewSet)
router.register('purchase-orders', views.PurchaseOrderViewset)
router.register('sales-orders', views.SalesOrderViewset)
router.register('payments', views.PaymentsViewset)



urlpatterns = router.urls