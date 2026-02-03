from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class UnitsMeasurement(models.Model):
    name = models.CharField(max_length=100, blank=False)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField()
    sku = models.CharField(max_length=255, unique=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    current_quantity = models.PositiveIntegerField( validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(default=0)
    buying_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    unit_of_measure = models.ForeignKey(UnitsMeasurement, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
   
class Supplier(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    products=models.ManyToManyField(Product)
    outstanding_balance=models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])

class Customer(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    products=models.ManyToManyField(Product)
    outstanding_balance=models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])

class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=255, unique=True, blank=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,null=False, blank=False )
    product=models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

class SalesOrder(models.Model):
    invoice_number = models.CharField(max_length=255, unique=True, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product=models.ForeignKey(Product, on_delete=models.PROTECT, null=False, blank=False)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    invoice_date = models.DateTimeField(auto_now_add=True)

class Payments(models.Model):
    PAYMENT_METHOD_CASH = 'CASH'
    PAYMENT_METHOD_CREDIT_CARD = 'CREDIT_CARD'
    PAYMENT_METHOD_BANK_TRANSFER = 'BANK_TRANSFER'

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CASH, 'Cash'),
        (PAYMENT_METHOD_CREDIT_CARD, 'Credit Card'),
        (PAYMENT_METHOD_BANK_TRANSFER, 'Bank Transfer')
    ]

    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    invoice_number = models.ForeignKey(SalesOrder.invoice_number, on_delete=models.PROTECT)
    order_number = models.ForeignKey(PurchaseOrder.order_number, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)