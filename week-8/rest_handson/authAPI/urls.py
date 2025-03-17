from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from authAPI.views import MyTokenObtainView

urlpatterns = [
    path('login/', MyTokenObtainView.as_view(), name='obtain-token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token')
]