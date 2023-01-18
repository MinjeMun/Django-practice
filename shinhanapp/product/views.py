from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import Product

# Create your views here.

def main(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'product.html', {'products':products})

def write(request): # 상품 등록하는 페이지
    if not request.user.is_authenticated:
        return redirect('/member/login/')

    if request.method == 'POST':
        product = Product(
            user=request.user, # 실시간 변경 데이터 반영
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            price=request.POST.get("price"),
            location=request.POST.get("location"),
            image=request.FILES.get("image"),
        )
        product.save() 
        return redirect('/')

    return render(request, 'product_write.html')

def detail(request, pk):
    product = Product.objects.get(pk=pk)

    ret = {
        'title': product.title,
        'username' : product.user.username, # 로그인 된 사용자 자동 로그인
        'content': product.content,
        'price': product.price,
        'location': product.location,
        'image' : '/static/bg.jpg',
    }

    if product.image:
        ret['image'] = product.image.url  


    return JsonResponse(ret)


    
# templates 폴더 만들고 index.html => 상품 리스트 표시
# main 함수 만들어서 상품 리스트 나오게 하기
# 상품 리스트에는 한줄로 상품명, 가격, 장소 나오게 하기