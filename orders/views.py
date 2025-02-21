from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Администратор видит все заказы, обычный пользователь – только свои
        if user.is_superuser or user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=user)
