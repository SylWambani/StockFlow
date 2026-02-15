from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('unit-measurements', views.UnitMeasurementViewSet)
router.register('products', views.ProductViewSet, basename='products')
router.register('product-variants', views.ProductVariantViewSet, basename='product-variants')
# router.register('product-value', views.ProductValueViewSet, basename='product-value')
router.register('stock-movement', views.StockMovementViewSet)

router.register('suppliers', views.SupplierViewSet)
router.register('customers', views.CustomerViewSet)
router.register('purchaseOrders', views.PurchaseOrderViewset)
router.register('salesOrders', views.SalesOrderViewset)
# router.register('payments', views.PaymentsViewset)

purchaseOrders_router = routers.NestedDefaultRouter(router, 'purchaseOrders', lookup='purchaseOrder')
purchaseOrders_router.register('purchase-orders-items', views.PurchaseOrderItemViewSet, basename='purchase-items')

salesOrders_router = routers.NestedDefaultRouter(router, 'salesOrders', lookup='salesOrder')
salesOrders_router.register('sales-orders-items', views.SalesOrderItemViewSet, basename='sales-items')

urlpatterns = router.urls + purchaseOrders_router.urls + salesOrders_router.urls