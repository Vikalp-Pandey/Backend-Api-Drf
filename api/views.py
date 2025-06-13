from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer)

# class ProductListCreateAPIView(generics.ListCreateAPIView):
#     #queryset = Product.objects.order_by('pk')
#     queryset = Product.objects.order_by('name')
    
#     serializer_class = ProductSerializer
#     filterset_class = ProductFilter
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#         InStockFilterBackend,
#     ]

#     # pagination_class = PageNumberPagination
#     pagination_class = LimitOffsetPagination
    
#     #pagination_class.page_size=2
#     #pagination_class.page_query_param='page_num'
#     #pagination_class.page_size_query_param="size"
#     #pagination_class.max_page_size=6


#     #search_fields = ['name', 'description']
#     search_fields = ['=name', 'description']
#     ordering_fields = ['name', 'price', 'stock']

#     def get_permissions(self):
#         self.permission_classes = [AllowAny]
#         if self.request.method == 'POST':
#             self.permission_classes = [IsAdminUser]
#         return super().get_permissions()

class ProductViewset(viewsets.ModelViewSet):
    #queryset = Product.objects.order_by('pk')
    queryset = Product.objects.order_by('name')
    
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]

    # pagination_class = PageNumberPagination
    pagination_class = LimitOffsetPagination
    
    #pagination_class.page_size=2
    #pagination_class.page_query_param='page_num'
    #pagination_class.page_size_query_param="size"
    #pagination_class.max_page_size=6


    #search_fields = ['name', 'description']
    search_fields = ['=name', 'description','id']
    ordering_fields = ['name', 'price', 'stock']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_url_kwarg = 'product_id'

#     def get_permissions(self):
#         self.permission_classes = [AllowAny]
#         if self.request.method in ['PUT', 'PATCH', 'DELETE']:
#             self.permission_classes = [IsAdminUser]
#         return super().get_permissions() 
       
class ProductDetailViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()    


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class=None
    filterset_class = OrderFilter
    filter_backends=[DjangoFilterBackend]
    
    def get_queryset(self):
        qs= super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs    
    # This method is used to filter orders by the authenticated user
    # It is called when the user accesses the 'user-orders' endpoint.So There is no need to define a viewset action for it like below
    
    
    @action(detail=False, methods=['get'],url_path='user-orders')
    def user_orders(self, request):
        # if not request.user.is_authenticated:
        #     return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
        
        user_orders = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_orders, many=True)
        return Response(serializer.data)


    

# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
    
class UserOrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
