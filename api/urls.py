from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

urlpatterns = [
    #path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    #path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    #path('orders/', views.OrderListAPIView.as_view()),
    #path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]

router=DefaultRouter()
router.register("products",views.ProductViewset, basename="products")
router.register("products-detail",views.ProductDetailViewset, basename="products-detail")
router.register("orders",views.OrderViewset,basename="orders")
router.register("user-orders",views.UserOrderViewset,basename="user-orders")
#router.register("user-orders",views.UserOrderViewset,basename="user-orders")
urlpatterns += router.urls

#     path('orders/', views.OrderViewset.as_view({'get': 'list', 'post': 'create'})),
