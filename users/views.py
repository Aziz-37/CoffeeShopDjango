from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

# POST /api/users/registration/
class RegistrationView(APIView):
    permission_classes = []  # Доступ без авторизации

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Пользователь зарегистрирован. Проверьте email для верификации.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST /api/users/verification/
class VerificationView(APIView):
    permission_classes = []  # Без авторизации, можно добавить проверку кода

    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            if user.is_verified:
                return Response({'message': 'Пользователь уже верифицирован.'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            return Response({'message': 'Пользователь верифицирован.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

# POST /api/users/me/
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# CRUD-операции над пользователями
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Просмотр списка и удаление доступны только администратору
        if self.action in ['list', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
