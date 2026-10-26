from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import MerchantSerializer, MerchantCreationSerializer, StoreSerializer, AdminStoreCreationSerializer
from .models import Merchant, Store
from .permissions import IsMerchant

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Merchant.objects.all()

        return Merchant.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return MerchantCreationSerializer
        else:
            return MerchantSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [IsMerchant]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Store.objects.all()

        return Store.objects.filter(owner=self.request.user.merchant)

    def get_serializer_class(self):
        if self.action == "create" and self.request.user.is_staff:
            return AdminStoreCreationSerializer
        else:
            return StoreSerializer
