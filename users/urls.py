from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView, VerificationView, MeView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('verification/', VerificationView.as_view(), name='verification'),
    path('me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]
