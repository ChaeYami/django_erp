
# Create your models here.
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
import uuid

class Product(models.Model):
    class Meta:
        db_table = "my_product"

    product_index = models.CharField(max_length=36, unique=True)
    product_codes = (
        ('hood-001', 'hood-001'),
        ('hood-002', 'hood-002'),
        ('hood-003', 'hood-003'),
        ('jean-001', 'jean-001'),
        ('socks-001', 'socks-001'),
        ('hat-001', 'hat-001'),
        
    )
    product_code = models.CharField(choices=product_codes, max_length=10)
    product_name = models.CharField(max_length=20)
    product_sizes = (
        ('XS', 'X-Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('F', 'Free'),
    )
    product_size = models.CharField(choices=product_sizes, max_length=2)
    product_price = models.CharField(max_length=10)
    product_desc = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    

    
    def __str__(self):
        return self.product_index

    def save(self, *args, **kwargs):
        if not self.id:  # 생성시 id가 없음 -> 생성동작
            self.product_index = str(uuid.uuid4())
            super().save(*args, **kwargs)
            Inventory.objects.create(product=self,product_index =self, stock=0)
        else:
            super().save(*args, **kwargs)

class Inventory(models.Model):
    class Meta:
        db_table = "my_inventory"
    
    
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    stock = models.IntegerField()
    product_index = models.CharField(max_length=36, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    
class Inbound(models.Model):
    class Meta:
        db_table = "my_inbound"
        
    product_index = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inbound_products',to_field='product_index',default=0)
    inbound_quantity = models.IntegerField(blank = True, default=0)
    inbound_date = models.DateTimeField(auto_now_add=True)
    

class Outbound(models.Model):
    class Meta:
        db_table = "my_outbound"
        
    product_index = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='outbound_products',to_field='product_index',default=0)
    outbound_quantity = models.IntegerField(blank = True, default=0)
    outbound_date = models.DateTimeField(auto_now_add=True)


