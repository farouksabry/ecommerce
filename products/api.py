from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from merchants.permissions import IsMerchant

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMerchant]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return Product.objects.all()
        else:
            if self.request.user.is_staff:
                return Product.objects.all()

            return Product.objects.filter(store__owner=self.request.user.merchant)
