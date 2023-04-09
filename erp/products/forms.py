import datetime
from time import timezone
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'product_size', 'product_price', 'product_desc']
        labels = {'product_code':'상품 코드' ,
                  'product_name' : '상품 이름',
                  'product_size' : '사이즈',
                  'product_price' : '가격',
                  'product_desc' : '상품 설명            '}

