from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

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
        if self.request.user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        order_items = self.get_object().items.all()
        if any(item.status != "ORDERED" for item in order_items):
            return Response({"This order cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()

        return OrderItem.objects.filter((
            Q(order__user=self.request.user) |
            Q(product__store__owner__user=self.request.user)
        ))

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser, IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return Response({"detail" : "This action is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        order_item = self.get_object()
        if order_item.order.user != request.user | order_item.status != "ORDERED":
            return Response({"This item cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
            
        return super().destroy(request, *args, **kwargs)
