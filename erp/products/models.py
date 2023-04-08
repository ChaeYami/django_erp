
# Create your models here.
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    class Meta:
        db_table = "my_product"

    product_code = models.CharField(max_length=10, unique=True)
    product_name = models.CharField(max_length=15)
    product_sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    product_size = models.CharField(choices=product_sizes, max_length=1)
    product_price = models.CharField(max_length=10)
    product_desc = models.TextField()

    def __str__(self):
        return self.product_code

    def save(self, *args, **kwargs):
        if not self.id:  # 생성시 id가 없음 -> 생성동작
            super().save(*args, **kwargs)
            Inventory.objects.create(product=self, quantity=0)
        else:
            super().save(*args, **kwargs)

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(blank = True,default=0)
    
    
class Inbound(Product):
    inbound_product_code = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inbound_products',to_field='product_code',default=0)
    inbound_quantity = models.IntegerField(blank = True, default=0)
    inbound_date = models.DateTimeField(auto_now_add=True)


class Outbound(Product):
    inbound_product_code = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='outbound_products',to_field='product_code',default=0)
    outbound_quantity = models.IntegerField(blank = True, default=0)
    outbound_date = models.DateTimeField(auto_now_add=True)


