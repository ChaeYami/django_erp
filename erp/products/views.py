from django.shortcuts import render, redirect
from .models import Inventory, Product, Inbound, Outbound
from django.contrib import auth  # 사용자 auth 기능(비밀번호 체크, 로그인 기능 해결)
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError


from .forms import  ProductForm

def home(request):
    user = request.user.is_authenticated # 로그인 여부 검증
    if user:
        return render(request, 'products/home.html')
    else:
        return redirect('/sign-in')
    
@login_required
def inventory_show(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            product_list = Inventory.objects.all()
        
            return render(request, 'products/inventory.html', {'product_list': product_list})
        else:
            return redirect('/sign-in')


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_list = Inventory.objects.all()
            return render(request, 'products/inventory.html', {'product_list': product_list})
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
        inbound = int(request.POST.get('inbound', ''))
        if product_code == '' or inbound == '':
            return render(request, 'products/inventory.html', {'error': 'Please fill all the fields'})
        else:
            
            inventory = Inventory.objects.get(product_code=product_code)
            
            inventory.stock += inbound # 재고량 증가
            inventory.save()
            
            return redirect('/inventory')
        

@login_required
def outbound_create(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            
            product_list = Product.objects.all()
            return render(request, 'products/outbound_create.html',{'product_list': product_list})
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        product_code = request.POST.get('product_code', '')
        outbound = request.POST.get('outbound', '')
        if product_code == '' or outbound == '':
            return render(request, 'products/inventory.html', {'error': 'Please fill all the fields'})
        else:
            inventory = Inventory.objects.get(product_code=product_code)
            
            inventory.stock -= int(outbound) # 재고량 감소
            inventory.save()
            
            return redirect('/inventory')
        
