import datetime
from time import timezone
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_code', 'product_name', 'product_size', 'product_price', 'product_desc')

    # def clean_product_code(self):
    #     product_code = self.cleaned_data.get('product_code')

    #     if Product.objects.filter(product_code=product_code).exists():
    #         raise forms.ValidationError("중복된 상품 코드입니다.")

    #     return product_code


