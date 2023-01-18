from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product

class ProductListView(APIView):
    def post(self, request, *args, **kwargs):
        product = Product(
            name=request.data.get('name'),
            price=request.data.get('price'),
            product_type=request.data.get('product_type'),
        )
        product.save() # pk는 save 될 때 만들어짐

        return Response({
            'id' : product.id,
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }, status=status.HTTP_201_CREATED)  

    
    def get(self, request, *args, **kwargs):
        ret = []
        # QuerySet - 여러개의 결과 값을 가져오는 것
        products = Product.objects.all()

        if 'price' in request.query_params:
            price = request.query_params['price']
            products = products.filter(price__lte=price)

        if 'name' in request.query_params:
            name = request.query_params['name']
            products = products.filter(name__contains=name)


        products = products.order_by('id')

        for product in products:
            p = {
            'id' : product.id, # id는 자동으로 생성됨
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
            }
            ret.append(p)    

        return Response(ret)


class ProductDetailView(APIView):
    # 1. get 하기 전에 exists()로 확인하고 가져오기
    # 2. get 할 때 예외처리 하기
    def get(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # 에러문 없이 status만 보여줌

        ret = {
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }

        return Response(ret)
        
    # delete() 함수를 이용해서 삭제
    # 삭제의 NO_CONTENT 204 상태 반환
    # 1. 없는데 지워졌다고 거짓말 하기 (204 반환)
    # 2. 없으면 없다고 반환하기 (404 반환)
    def delete(self, request, pk, *args, **kwargs):
        if Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)  

    # Product 객체 가져와야 함
    # request.data에 데이터가 들어있음
    # request.data에 "모든 데이터"가 있는 건 아님
    # 값을 수정할 때는 객체 안에 있는 변수의 값을 바꾸면 됨
    # 값을 수정한 결과를 database에 반영 (save 함수)
    def put(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        dirty = False # 수정 여부 확인하는 변수

        # field가 Product에 없는 값이 와야 한다.
        # save라는 field가 생기면 save 함수를 사용할 수 없어짐
        for field, value in request.data.items():
            if field not in [f.name for f in product._meta.get_fields()]:
                continue
            # getattr() 값을 가지고 옴 (수정된 게 하나라도 있으면 dirty = True)
            dirty = dirty or (value != getattr(product, field))
            setattr(product, field, value) 
        
        if dirty:
            product.save() # 변경된 게 있으면 save() 실행

        return Response()   


        


