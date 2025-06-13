import django_filters
from api.models import Product,Order
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self,request,queryset,view):
        return queryset.filter(stock__gt=0)





class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range'],
            'id': ['exact', 'in'],
        }
        #Same Fields as in ProductModel/Serializer

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact', 'contains'],
            'created_at': ['lt', 'gt','iexact'],
        }
        #Filtering fields for Order model
        #Same Fields as in OrderModel/Serializer