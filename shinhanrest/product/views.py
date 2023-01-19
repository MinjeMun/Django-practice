from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer
from.paginations import ProductLargePagination

# 상속을 여러개 받음 (부모-자식이랑은 좀 다른 관계)

class ProductListView(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,     
    generics.GenericAPIView
): 
    serializer_class = ProductSerializer
    pagination_class = ProductLargePagination


    def get_queryset(self):
        products = Product.objects.all()
        name = self.request.query_params.get('name')

        if name:
            products = products.filter(name__contains=name)
        
        return products.order_by('id')


    def get(self, request, *args, **kwargs):
        print(request.user)
        return self.list(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

class ProductDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, args, kwargs)