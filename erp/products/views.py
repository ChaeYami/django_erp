from django.shortcuts import render, redirect
from .models import Product, Inbound, Outbound
from django.http import HttpResponse
from django.contrib import auth  # 사용자 auth 기능(비밀번호 체크, 로그인 기능 해결)
from django.contrib.auth.decorators import login_required


from .forms import  ProductForm

def home(request):
    user = request.user.is_authenticated # 로그인 여부 검증
    if user:
        return render(request, 'products/home.html')
    else:
        return redirect('/sign-in')

def inventory_show(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            product_list = Product.objects.all()
        
            return render(request, 'products/inventory.html', {'product_list': product_list})
        else:
            return redirect('/sign-in')



@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_list = Product.objects.all()
            return render(request, 'products/inventory.html', {'product_list': product_list})
        else:
            return render(request, 'products/product_create.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'products/product_create.html', {'form': form})


@login_required
def inbound_create(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            
            product_list = Product.objects.all()
            return render(request, 'products/inbound_create.html',{'product_list': product_list})
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        product_code = request.POST.get('product_code', '')
        inbound = request.POST.get('inbound', '')
        if product_code == '' or inbound == '':
            return render(request, 'products/inventory.html', {'error': 'Please fill all the fields'})
        else:
            product = Product.objects.get(product_code=product_code)
            
            product.stock += int(inbound) # 재고량 증가
            product.save()
            return redirect('/inventory')
        
# @login_required
# def inbound_create(request):
#     if request.method == 'GET':
#         product_list = Product.objects.all()
#         form = InboundForm()
#         return render(request, 'products/inbound_create.html', {'product_list': product_list, 'form': form})

#     elif request.method == 'POST':
#         form = InboundForm(request.POST)
#         if form.is_valid():
#             product_code = form.cleaned_data['product_code']
#             inbound_quantity = form.cleaned_data['product_quantity']
#             product = Product.objects.get(product_code=product_code)
#             product.product_quantity += int(inbound_quantity)
#             product.save()
#             product_list = Product.objects.all()
#             inbound_date = Inbound.objects.inbound_date

#             return render(request, 'products/inventory.html', {'product_list': product_list, 'inbound_date': inbound_date})
#         else:
#             product_list = Product.objects.all()
#             return render(request, 'products/inbound_create.html', {'product_list': product_list, 'form': form})



