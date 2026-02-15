from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Sum, F, DecimalField
from django.db.models.aggregates import Count
from .models import Category, Customer, Product, ProductVariant, PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem, StockMovement, Supplier, UnitsMeasurement
from .serializers import CategorySerializer, CustomerSerializer, ProductSerializer, ProductVariantSerializer, PurchaseOrderItemSerializer, PurchaseOrderSerializer, SalesOrderItemSerializer, SalesOrderSerializer, StockMovementSerializer, SupplierSerializer, UnitMeasurementSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('product')).all()
    serializer_class = CategorySerializer

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class UnitMeasurementViewSet(ModelViewSet):
    queryset = UnitsMeasurement.objects.all()
    serializer_class = UnitMeasurementSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class StockMovementViewSet(ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class PurchaseOrderViewset(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderItemViewSet(ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer

class SalesOrderViewset(ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer

class SalesOrderItemViewSet(ModelViewSet):
    queryset = SalesOrderItem.objects.all()
    serializer_class = SalesOrderItemSerializer
    
# class ProductValueViewSet(ReadOnlyModelViewSet):
#     serializer_class = ProductValueSerializer

#     def get_queryset(self):
#         return Product.objects.select_related('category').all()
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()

#         serializer = self.get_serializer(queryset, many=True)

#         category_values = (
#             queryset
#             .values(category_name=F('category__name'))
#             .annotate(
#                 total_value=Sum(
#                     F('current_quantity') * F('buying_price'),
#                     output_field=DecimalField()
#                 )
#             )
#             .order_by('category_name')
#         )

#         total_value = queryset.aggregate(
#             total=Sum(
#                 F('current_quantity') * F('buying_price'),
#                 output_field=DecimalField()
#             )
#         )['total'] or 0

#         return Response({
#             "total_inventory_value": total_value,
#             "categories": category_values,
#             "products": serializer.data
#         })
    
    






# class PaymentsViewset(ModelViewSet):
#     queryset = Payments.objects.all()
#     serializer_class = PaymentsSerializer