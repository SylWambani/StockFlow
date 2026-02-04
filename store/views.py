from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.db.models.aggregates import Count
from .models import Category, Customer, Payments, Product, PurchaseOrder, SalesOrder, Supplier, UnitsMeasurement
from .serializers import CategorySerializer, CustomerSerializer, PaymentsSerializer, ProductSerializer, PurchaseOrderSerializer, SalesOrderSerializer, SupplierSerializer, UnitMeasurementSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('product')).all()
    serializer_class = CategorySerializer

class UnitMeasurementViewSet(ModelViewSet):
    queryset = UnitsMeasurement.objects.all()
    serializer_class = UnitMeasurementSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class PurchaseOrderViewset(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class SalesOrderViewset(ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer

class PaymentsViewset(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer