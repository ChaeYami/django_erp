import datetime
from time import timezone
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_code', 'product_name', 'product_size', 'product_price', 'product_desc')



