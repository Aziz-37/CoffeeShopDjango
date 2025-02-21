from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import  get_schema_view
from drf_yasg import openapi

def home_view(request):
    return HttpResponse("Hello from the main page!")

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

schema_view = get_schema_view(
   openapi.Info(
      title="Coffee Shop API",
      default_version='v1',
      description="Документация для API кофейни",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/static-info/', include('static_info.urls')),
]
