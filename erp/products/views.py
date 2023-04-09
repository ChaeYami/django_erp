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
    
@login_required(login_url='/sign-in') # 로그인을 하지 않고 url을 통해 접속할 경우 리디렉션 
def inventory_show(request):
    if request.method == 'GET': # 제품목록을 보여주는 함수이므로 GET만 사용함
        user = request.user.is_authenticated #로그인 여부
        
        if user: #로그인이 되어있다면
            product_list = Inventory.objects.all().order_by('-updated_at')
            # 제품 목록을 업데이트 내림차순으로 저장한다.
            # 제품 목록을 템플릿에 전달
            return render(request, 'products/inventory.html', {'product_list': product_list})
        
        else: # 로그인이 안 돼있다면 로그인 페이지로
            return redirect('/sign-in')


@login_required(login_url='/sign-in') # 로그인을 하지 않고 url을 통해 접속할 경우 리디렉션
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_list = Inventory.objects.all().order_by('-updated_at')
            return render(request, 'products/inventory.html', {'product_list': product_list})
    else:
        form = ProductForm()
        
    return render(request, 'products/product_create.html', {'form': form})


@login_required(login_url='/sign-in') # 로그인을 하지 않고 url을 통해 접속할 경우 리디렉션
def inbound_create(request):
    
    if request.method == 'GET':
        user = request.user.is_authenticated
        
        if user: # 로그인 여부
            
            product_list = Inventory.objects.all().order_by('-updated_at') # 제품목록 보여주기
            
            return render(request, 'products/inbound_create.html',{'product_list': product_list}) 
            # 제품 목록을 html로 가지고 감 
            
        else: # 로그인이 안 되어있다면
            return redirect('/sign-in') #로그인 화면으로
        
    elif request.method == 'POST':
        
        # 인덱스와 입고량을 사용자에게 받아옴
        product_index = request.POST.get('product_index', '') # 사용자가 선택한 제품의 인덱스를 받아온다.
        inbound = request.POST.get('inbound', '') # 사용자가 입력한 입고량
        
        if product_index == '' or inbound == '': # 입력된 값이 없을 때
            
            product_list = Inventory.objects.all().order_by('-updated_at')            
            # 제품 목록을 html로 가지고 가면서 에러메시지 띄우기
            return render(request, 'products/inbound_create.html', {'product_list': product_list,'error': '내용을 입력해주세요.'})
        else:
            # 인덱스값 비교해서 
            inventory = Inventory.objects.get(product_index=product_index)
            inventory.stock += int(inbound) # 해당 제품의 재고량 증가
            inventory.save()
            
            return redirect('/inventory')
        

@login_required(login_url='/sign-in') # 로그인을 하지 않고 url을 통해 접속할 경우 리디렉션
def outbound_create(request):
    
    if request.method == 'GET':
        user = request.user.is_authenticated
        
        if user: # 로그인 여부
            
            product_list = Inventory.objects.all().order_by('-updated_at') # 제품목록 보여주기
            
            # 제품 목록을 html로 가지고 감 
            return render(request, 'products/outbound_create.html',{'product_list': product_list})
        
        else: # 로그인이 안 되어있다면
            return redirect('/sign-in') #로그인 화면으로
        
    elif request.method == 'POST':
        
        # 인덱스와 입고량을 사용자에게 받아옴
        product_index = request.POST.get('product_index', '') # 사용자가 선택한 제품의 인덱스를 받아온다.
        outbound = request.POST.get('outbound', '') # 사용자가 입력한 출고량
        
        if product_index == '' or outbound == '': # 입력된 값이 없을 때
            product_list = Inventory.objects.all().order_by('-updated_at')            
            # 제품 목록을 html로 가지고 가면서 에러메시지 띄우기
            return render(request, 'products/outbound_create.html', {'product_list': product_list,'error': '내용을 입력해주세요.'})
        else:
            # 인덱스값 비교해서 
            inventory = Inventory.objects.get(product_index=product_index)
            
            if int(outbound) > inventory.stock:  # 출고하려는 수량이 재고보다 많을 경우
                product_list = Inventory.objects.all().order_by('-updated_at')
                # 제품 목록을 html로 가지고 가면서 에러메시지 띄우기
                return render(request, 'products/outbound_create.html', {'product_list': product_list,'error': '출고량은 재고량보다 많을 수 없습니다.'})
            
            inventory.stock -= int(outbound) # 해당 제품 재고량 감소
            inventory.save()
            
            return redirect('/inventory')
        
