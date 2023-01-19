from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=128, verbose_name='상품명')
    price=models.IntegerField(verbose_name='가격')
    product_type = models.CharField(max_length=8, verbose_name='상품유형',
        choices=( 
            ('단품','단품'), # (db)값, (display)값
            ('세트','세트'),
        )
    )
    # 넣는 시점에 시간(날짜) 들어감
    tstamp = models.DateTimeField(auto_now_add=True, verbose_name='등록일시') 

    class Meta:
        db_table = 'shinhan_product'
        verbose_name = '상품'
        verbose_name_plural = '상품'

# 댓글 모델 만들기
# field로 사용자 외래키, 상품 외래키, 댓글 내용, tstamp
# 관리자 페이지에 등록해서
# 관리자 페이지를 통해 댓글 3개 작성

class Comment(models.Model):
    # Member를 사용하기 위해 member.Member로 참조함 - 양 쪽 models에 import를 하게 되면 순환참조로 인해 오류 발생할 수 있음
    user = models.ForeignKey('member.Member', on_delete=models.CASCADE, verbose_name='사용자') 
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')
    reply = models.TextField(verbose_name='댓글')
    tstamp = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

    class Meta:
        db_table = 'shinhan_comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
