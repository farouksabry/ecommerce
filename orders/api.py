from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser, IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.all()
