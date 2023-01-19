from rest_framework import serializers
from .models import Product,Comment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__' # 리스트로 원하는 field만 작성도 가능

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = '__all__' # 리스트로 원하는 field만 작성도 가능
