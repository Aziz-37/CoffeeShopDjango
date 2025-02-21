from django.urls import path
from .views import StaticInfoView

urlpatterns = [
    path('', StaticInfoView.as_view(), name='static-info'),
]
