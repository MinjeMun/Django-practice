from django.urls import path
from . import views

urlpatterns = [
    path("/<int:pk>", views.ProductDetailView.as_view()),
    path("", views.ProductListView.as_view()),
    #행동이 resource가 되면 안됨 -> /~ 경로로 추가하면 restful 하지 못함
]
