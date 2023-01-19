from rest_framework import generics, mixins
from .models import Product, Comment
from .serializers import ProductSerializer, CommentSerializer
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
        if self.request.user.is_authenticated: # 로그인 검사
            products = Product.objects.all()
        else:
            products = Product.objects.none()
        
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

class CommentListView(
    mixins.ListModelMixin,    
    generics.GenericAPIView
): 
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all().order_by('id')


    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

class CommentDetailView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = CommentSerializer

    def get_queryset(self, pk):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(pk=product_id)

    def get(self, request, pk, *args, **kwargs):
        return self.list(request, args, kwargs)