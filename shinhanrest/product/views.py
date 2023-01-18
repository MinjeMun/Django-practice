from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product

class ProductTempView(APIView): # 메서드에 대한 코드 작성
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=1)

        ret = {
            '상품명': product.name,
            '가격': product.price,
            '타입': product.product_type,
        }

        return Response(ret)