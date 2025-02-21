from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Привязываем элемент к текущему пользователю
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # DELETE /api/cart/clear/ для очистки всей корзины
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        self.get_queryset().delete()
        return Response({'message': 'Корзина очищена.'}, status=status.HTTP_204_NO_CONTENT)
