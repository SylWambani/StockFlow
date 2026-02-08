from rest_framework import serializers
from decimal import Decimal
from django.db.models.aggregates import Count, Sum
from .models import Category, Customer, Payments, Product, PurchaseOrder, SalesOrder, Supplier, UnitsMeasurement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count', 'total_category_inventory']

    products_count = serializers.IntegerField(read_only=True)
    total_category_inventory = serializers.SerializerMethodField()

    def get_total_category_inventory(self, obj):
        return obj.product_set.aggregate(total=Sum('current_quantity'))['total'] or 0  
    
class UnitMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitsMeasurement
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.ReadOnlyField()
    category = serializers.StringRelatedField()
    unit_of_measure = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ['id', 'name','sku', 'category', 'current_quantity', 'reorder_level', 'buying_price', 'selling_price', 'unit_of_measure', 'is_active']
        
class ProductValueSerializer(serializers.ModelSerializer):
    product_value = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields=['id', 'name', 'category', 'current_quantity', 'buying_price', 'product_value']

    def get_product_value(self, product:Product):
        return product.current_quantity * product.buying_price

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