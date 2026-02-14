import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
#from .utils import create_unique_code

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class UnitsMeasurement(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField()
    #sku = models.CharField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    #current_quantity = models.PositiveIntegerField( validators=[MinValueValidator(0)])
    #reorder_level = models.IntegerField(default=0)
    unit_of_measure = models.ForeignKey(UnitsMeasurement, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if not self.short_code:
    #         self.short_code = create_unique_code()

    #     if not self.sku:
    #         cat = self.category.name[:3].upper()
    #         name = self.name[:3].upper()

    #         base_sku = f"{cat}-{name}-{self.short_code}"

    #         self.sku=base_sku
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")

    sku = models.CharField(max_length=50, unique=True, editable=False)
    short_code = models.CharField(max_length=8, unique=True, editable=False)

    # Optional attributes
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    buying_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])

    reorder_level = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'],
                name='unique_variant_per_product'
            )
        ]

    def clean(self):
        if ProductVariant.objects.filter(
            product=self.product,
            color=self.color,
            size=self.size
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "You already created an SKU for this product variant."
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk:
            cat = self.product.category.name[:3].upper()
            name = self.product.name[:3].upper()
            self.short_code = uuid.uuid4().hex[:8].upper()
            self.sku = f"{cat}-{name}-{self.short_code}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.sku}"
    
    


   
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
    invoice_number = models.ForeignKey(SalesOrder, on_delete=models.PROTECT)
    order_number = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)