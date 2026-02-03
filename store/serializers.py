from rest_framework import serializers
from decimal import Decimal
from .models import Category, Customer, Payments, Product, PurchaseOrder, SalesOrder, Supplier, UnitsMeasurement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

class UnitMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitsMeasurement
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'category', 'current_quantity', 'reorder_level', 'buying_price', 'selling_price', 'unit_of_measure', 'is_active']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields = ['id', 'name', 'email', 'phone', 'products', 'outstanding_balance']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = ['id', 'name', 'email', 'phone', 'products', 'outstanding_balance']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'product', 'quantity', 'price_per_unit', 'total_amount', 'order_date']

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=SalesOrder
        fields = ['id', 'invoice_number', 'customer', 'product', 'quantity', 'price_per_unit', 'total_amount', 'invoice_date']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields=['id', 'payment_date', 'amount', 'payment_method', 'invoice_number', 'order_number', 'supplier', 'customer']